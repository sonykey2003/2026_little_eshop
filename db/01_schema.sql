-- ---------------------------------------------------------------------------
-- The shape of our data.
--
-- A database stores information in TABLES. A table is a grid: the columns
-- say what kind of information we keep, and each row is one real thing.
--
-- This file runs automatically the first time the database starts.
-- ---------------------------------------------------------------------------


-- Everything the shop sells. One row = one product.
CREATE TABLE products (
    id          SERIAL PRIMARY KEY,   -- a unique number, counted up for us
    name        TEXT NOT NULL,        -- NOT NULL means "this can never be empty"
    description TEXT NOT NULL,
    price       NUMERIC(10, 2) NOT NULL,  -- up to 10 digits, 2 after the point
    image_file  TEXT NOT NULL,        -- which picture in app/static/img to show
    in_stock    BOOLEAN NOT NULL DEFAULT TRUE
);


-- One row every time somebody completes the checkout.
CREATE TABLE orders (
    id            SERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email         TEXT NOT NULL,
    total         NUMERIC(10, 2) NOT NULL,
    placed_at     TIMESTAMP NOT NULL DEFAULT NOW()

    -- Notice what is NOT here: no card number, no address, no password.
    -- The safest way to protect information is to never collect it.
);


-- The individual lines inside one order: "2 x Woven Sun Hat".
--
-- We keep this separate from the orders table because one order can hold
-- many different products. Splitting it like this is called NORMALISATION.
CREATE TABLE order_items (
    id         SERIAL PRIMARY KEY,

    -- REFERENCES ties this row to a real order. The database will now
    -- refuse to store an order_item pointing at an order that
    -- does not exist, which keeps our data honest.
    order_id   INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),

    quantity   INTEGER NOT NULL,

    -- We copy the price in at the moment of sale. If we later change the
    -- price of a sun hat, old orders must still show what was actually paid.
    unit_price NUMERIC(10, 2) NOT NULL
);
