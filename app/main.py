"""
The shop itself.

Every page of the website is one function below. The @app.route line above
each function says which web address runs it.

Read this file from top to bottom and you have read the whole website.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify

import chatbot
import database
import settings

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY


# ---------------------------------------------------------------------------
# Shared values
# ---------------------------------------------------------------------------

@app.context_processor
def values_every_page_needs():
    """
    Anything returned here can be used in any HTML template without
    passing it in by hand every single time. The shop name is in the
    header of every page, so this saves a lot of repetition.
    """
    return {
        "shop_name": settings.SHOP_NAME,
        "shop_tagline": settings.SHOP_TAGLINE,
        "currency": settings.CURRENCY_SYMBOL,
        "chat_enabled": chatbot.is_enabled(),
        "cart_count": sum(get_cart().values()),
    }


# ---------------------------------------------------------------------------
# The shopping cart
# ---------------------------------------------------------------------------
# The cart lives in the visitor's "session": a small, signed cookie in their
# browser. It is not in the database, because an abandoned cart is nobody's
# business but the shopper's.
#
# It is stored as {"3": 2} meaning "two of product number 3".

def get_cart():
    """The current visitor's cart. An empty dictionary if they have none."""
    return session.get("cart", {})


def save_cart(cart):
    """Put the cart back into the session cookie."""
    session["cart"] = cart


def get_cart_lines():
    """
    Turn the bare {"3": 2} cart into something a page can display:
    the full product details, the quantity, and the price for that line.
    """
    lines = []

    for product_id, quantity in get_cart().items():
        product = database.get_product(int(product_id))

        # The product may have been deleted since it went in the cart.
        if product is None:
            continue

        lines.append({
            "product": product,
            "quantity": quantity,
            "line_total": product["price"] * quantity,
        })

    return lines


def get_cart_total(lines):
    """Add up every line in the cart."""
    return sum(line["line_total"] for line in lines)


# ---------------------------------------------------------------------------
# The pages
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """The front page: every product we sell."""
    return render_template("index.html", products=database.get_all_products())


@app.route("/product/<int:product_id>")
def product_page(product_id):
    """One product, in detail."""
    product = database.get_product(product_id)

    if product is None:
        # Flask turns this number into a "404 Not Found" page.
        return render_template("not_found.html"), 404

    return render_template("product.html", product=product)


@app.route("/cart")
def cart_page():
    """Everything the visitor has picked so far."""
    lines = get_cart_lines()
    return render_template("cart.html", lines=lines, total=get_cart_total(lines))


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    """Add one of this product to the cart, then go to the cart page."""
    cart = get_cart()

    # Dictionary keys from a cookie are always text, so we use str() to
    # make sure "3" and 3 do not end up as two separate items.
    key = str(product_id)
    cart[key] = cart.get(key, 0) + 1

    save_cart(cart)
    return redirect(url_for("cart_page"))


@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    """Take this product out of the cart completely."""
    cart = get_cart()
    cart.pop(str(product_id), None)

    save_cart(cart)
    return redirect(url_for("cart_page"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    """
    Show the checkout form, and handle it when it is sent back.

    One function serves both: a GET request means "show me the form",
    a POST request means "here are my answers".
    """
    lines = get_cart_lines()

    # Nothing to buy, so there is nothing to check out.
    if not lines:
        return redirect(url_for("home"))

    total = get_cart_total(lines)

    if request.method == "POST":
        order_id = database.create_order(
            customer_name=request.form["customer_name"],
            email=request.form["email"],
            cart_lines=lines,
            total=total,
        )

        # The card number typed into the form is deliberately ignored.
        # It is never read, never stored, never sent anywhere. This shop
        # is a demo, and a demo has no business handling real card details.

        session.pop("cart", None)      # the cart is now an order
        return redirect(url_for("order_confirmed", order_id=order_id))

    return render_template("checkout.html", lines=lines, total=total)


@app.route("/order/<int:order_id>")
def order_confirmed(order_id):
    """The thank-you page shown after a pretend payment."""
    order = database.get_order(order_id)

    if order is None:
        return render_template("not_found.html"), 404

    return render_template("order_confirmed.html", order=order)


# ---------------------------------------------------------------------------
# The optional AI assistant
# ---------------------------------------------------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    The chat box in the corner of the page sends messages here.

    This address returns JSON rather than a web page, because JavaScript
    in the browser is reading it, not a person.
    """
    if not chatbot.is_enabled():
        return jsonify({"reply": "The AI assistant is switched off."})

    conversation = request.json.get("messages", [])
    return jsonify({"reply": chatbot.ask(conversation)})


# ---------------------------------------------------------------------------
# Starting the app
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # host="0.0.0.0" lets the page be reached from outside the container.
    # debug=True reloads the app whenever you save a file, and shows the
    # full error when something breaks. Both are wonderful while learning
    # and must never be used on a real public website.
    app.run(host="0.0.0.0", port=8000, debug=True)
