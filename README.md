# The Little Shop

A small online shop, written in Python, built to be read.

You get a product catalogue, a shopping cart, a pretend checkout, a real
database, and an optional AI assistant. Everything runs on your own laptop
inside Docker, so there is nothing to install beyond Docker itself.

Nothing here is really for sale and no payment is ever taken.

---

## 1. Run it

You need **Docker Desktop**, running. That is the only requirement.

> **Coming to the workshop?** Do the downloads at home first.
> [PREPARE.md](PREPARE.md) walks you through it. The venue wifi is shared
> between everyone in the room, and this is about 165 MB each.

```bash
git clone <the address of this repository>
cd <the folder it made>

cp .env.example .env          # your own settings; Windows: copy .env.example .env

docker compose up
```

The first run takes a few minutes while Docker downloads Python and
PostgreSQL. Later runs take seconds.

When the terminal settles down, open **<http://localhost:8000>**.

To stop it, press `Ctrl+C` in that terminal.

| Command | What it does |
| --- | --- |
| `docker compose up` | Start the shop |
| `docker compose up --build` | Start it after you changed `requirements.txt` or the `Dockerfile` |
| `docker compose down` | Stop it, keep the data |
| `docker compose down -v` | Stop it and **erase the database**, so `db/` runs again |
| `docker compose logs -f web` | Watch the website's messages |

### If something goes wrong

**"port is already allocated"** — something else on your laptop is using
port 8000 or 5432. Change the left-hand number in `docker-compose.yml`,
for example `"8001:8000"`, and use <http://localhost:8001> instead.

**The page will not load** — give it another few seconds. The website waits
for the database to be ready before it starts.

**You changed a `.sql` file and nothing happened** — those files only run
when the database is brand new. Run `docker compose down -v` and start again.

---

## 2. What is in here

```
.
├── app/                    the website
│   ├── main.py             every page, one function each   <- start reading here
│   ├── database.py         all of the SQL
│   ├── chatbot.py          the optional AI assistant
│   ├── settings.py         every setting, in one place
│   ├── templates/          the HTML
│   └── static/
│       ├── style.css       all of the styling              <- start editing here
│       ├── chat.js         the chat box
│       └── img/            placeholder product pictures
├── db/
│   ├── 01_schema.sql       the shape of the data
│   └── 02_seed_data.sql    the products you start with
├── Dockerfile              how the website gets built
├── docker-compose.yml      how the website and database fit together
├── PREPARE.md              what to download before the workshop
└── .env                    your settings (never shared)
```

Two programs are running: the **web** container with your Python in it, and
the **db** container holding PostgreSQL. They find each other by name.

Your `app/` folder is shared live with the running container. Save a Python,
HTML or CSS file and refresh the browser: the change is already there. You
only need `--build` when the libraries or the `Dockerfile` change.

---

## 3. Make it yours

### The name, tagline and currency

Open `.env` and edit the top three lines, then restart with
`docker compose up`.

```env
SHOP_NAME="Sam's Surf Shack"
SHOP_TAGLINE="Boards, wax and sunburn"
CURRENCY_SYMBOL="$"
```

### The colours and the layout

Open **`app/static/style.css`**. The first block is a list of colours and
sizes used everywhere else:

```css
:root {
  --brand:      #0f766e;   /* buttons, links, the shop name */
  --page:       #f8fafc;   /* the background behind everything */
  --radius:     10px;      /* how rounded the corners are. Try 0. Try 30px. */
}
```

Change one value, save, refresh. One edit reaches every page at once.

The rest of the file is grouped by what it styles — header, products,
buttons, cart — so you can find things by name.

### The products

Open **`db/02_seed_data.sql`** and edit the list. Add rows, remove rows,
change the prices. Then rebuild the database:

```bash
docker compose down -v
docker compose up
```

For pictures, drop your own files into `app/static/img/` and put the
filename in the `image_file` column.

### The words on the pages

The HTML lives in `app/templates/`. `base.html` is the frame every page
sits in (the header, the footer); the others fill in the middle.

### The pages themselves

`app/main.py`. Each page is a function with a `@app.route(...)` line above
it saying which address runs it. Copy an existing one to add a new page.

---

## 4. Look inside the database

The data is real PostgreSQL, and you can talk to it directly. With the
shop running, open a second terminal:

```bash
docker compose exec db psql -U shopkeeper -d shop
```

You are now at a `shop=#` prompt. Try these:

```sql
\dt                                         -- list the tables
SELECT * FROM products;                     -- everything we sell
SELECT name, price FROM products ORDER BY price DESC;
SELECT * FROM products WHERE price < 300;
SELECT * FROM orders;                       -- empty until you buy something
```

Every query ends with a semicolon. Type `\q` to leave.

---

## 5. The optional AI assistant

Off by default. With no key, the chat button never appears and the shop
works exactly as before.

**Step 1. Get a free key** from either one:

- **NVIDIA NIM** — <https://build.nvidia.com/>
- **OpenRouter** — <https://openrouter.ai/>

**Step 2. Put it in `.env`.** Uncomment one block and paste your key in:

```env
# NVIDIA NIM
AI_API_KEY=nvapi-your-key-here
AI_BASE_URL=https://integrate.api.nvidia.com/v1
AI_MODEL=meta/llama-3.1-8b-instruct
```

```env
# OpenRouter
AI_API_KEY=sk-or-your-key-here
AI_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

**Step 3. Restart.**

```bash
docker compose up
```

An **Ask for help** button now sits in the bottom right corner.

To change its personality, edit `SYSTEM_PROMPT` at the top of
`app/chatbot.py`.

To switch it off again, blank out `AI_API_KEY` and restart.

### Keep your key to yourself

An API key is a password that spends money. `.env` is listed in
`.gitignore`, so it never leaves your laptop — **keep it that way**. If a
key ever does get published, go to the website you got it from and delete
it immediately. Never paste a key into `settings.py`, a template, or a
screenshot.

---

## 6. Things this shop does safely, and why

Worth knowing, because getting these wrong is how real shops get broken
into.

**Values are never glued into SQL.** Every query in `database.py` passes
its values separately:

```python
conn.execute("SELECT ... WHERE id = %s", (product_id,))   # safe
```

The database then treats them as data and never as instructions. Building
the query by joining strings is called *SQL injection*, and it is one of
the oldest ways to empty a database.

**The card number is never read.** The checkout form has a card box so the
page looks finished. `main.py` ignores it. Nothing to store is nothing to
leak.

**We collect almost nothing.** A name, an email, and what was bought. No
address, no password, no card.

**The AI key stays on the server.** The browser talks to our own
`/api/chat`; only the Python code knows the key.

**The container does not run as root.** The `Dockerfile` creates a normal
user and switches to it.

**This is still a practice app.** `debug=True` in `main.py` shows anyone
your code when something breaks, and Flask's built-in server is not built
for real traffic. Both are perfect for learning and wrong for the public
internet.
