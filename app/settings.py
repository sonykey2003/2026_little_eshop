"""
Every setting for the shop, in one place.

Each line reads an environment variable (set in your .env file) and falls
back to a sensible default if you have not set one. That means the app
always runs, even with no configuration at all.
"""

import os


# ---------------------------------------------------------------------------
# Your shop. Change these first.
# ---------------------------------------------------------------------------

SHOP_NAME = os.environ.get("SHOP_NAME")
SHOP_TAGLINE = os.environ.get("SHOP_TAGLINE")
CURRENCY_SYMBOL = os.environ.get("CURRENCY_SYMBOL")


# ---------------------------------------------------------------------------
# The database.
# ---------------------------------------------------------------------------
# "db" is the name of the database service in docker-compose.yml.
# Docker turns that name into an address for us.

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://shopkeeper:shoppassword@db:5432/shop",
)


# ---------------------------------------------------------------------------
# Flask.
# ---------------------------------------------------------------------------
# The secret key signs the cookie that remembers your shopping cart, so
# nobody can edit their own cart by hand. A real shop keeps this secret.

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")


# ---------------------------------------------------------------------------
# The optional AI assistant.
# ---------------------------------------------------------------------------
# Leave AI_API_KEY empty and the chat button never appears.
# See README.md for how to switch it on.

AI_API_KEY = os.environ.get("AI_API_KEY", "")
AI_BASE_URL = os.environ.get("AI_BASE_URL", "")
AI_MODEL = os.environ.get("AI_MODEL", "")
