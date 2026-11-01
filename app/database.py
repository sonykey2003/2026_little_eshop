"""
Everything that talks to the database.

Keeping all the SQL in one file means that when you want to change what the
shop knows, you only have one place to look.
"""

import psycopg
from psycopg.rows import dict_row

from settings import DATABASE_URL


def get_connection():
    """
    Open a fresh connection to the database.

    row_factory=dict_row asks psycopg to hand each row back as a dictionary,
    so we can write product["name"] instead of counting columns: product[1].
    """
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def get_all_products():
    """Return every product, cheapest first."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, name, description, price, image_file, in_stock
            FROM products
            ORDER BY price
            """
        ).fetchall()


def get_product(product_id):
    """Return one product, or None if there is no product with that id."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT id, name, description, price, image_file, in_stock
            FROM products
            WHERE id = %s
            """,
            # The comma matters: (product_id,) is a tuple of one item.
            #
            # Notice we pass the value separately instead of gluing it into
            # the text of the query. The database then treats it as data and
            # never as an instruction. Gluing user input into SQL is how
            # websites get broken into. It is called SQL injection, and this
            # one habit prevents it.
            (product_id,),
        ).fetchone()


def create_order(customer_name, email, cart_lines, total):
    """
    Save a completed order and return its new id.

    cart_lines is a list of dictionaries, each with a "product" and a
    "quantity", exactly as main.py builds it for the cart page.
    """
    with get_connection() as conn:
        # Write the order itself first, because every order_item below needs
        # to point at it. RETURNING id asks PostgreSQL for the number it just
        # created, saving us a second query.
        order = conn.execute(
            """
            INSERT INTO orders (customer_name, email, total)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (customer_name, email, total),
        ).fetchone()

        order_id = order["id"]

        # Then write one row per product in the cart.
        for line in cart_lines:
            conn.execute(
                """
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
                """,
                (order_id, line["product"]["id"], line["quantity"], line["product"]["price"]),
            )

        # Leaving the "with" block saves all of the above together.
        # If any line had failed, none of it would be saved. All or nothing.

    return order_id


def get_order(order_id):
    """Return one order, or None."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, customer_name, email, total, placed_at FROM orders WHERE id = %s",
            (order_id,),
        ).fetchone()
