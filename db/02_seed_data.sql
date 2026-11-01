-- ---------------------------------------------------------------------------
-- Some products to get started with.
--
-- These are placeholders. Change the names, descriptions and prices to
-- whatever your shop sells. Add rows, delete rows, it is your shop.
--
-- After editing this file you need a fresh database:
--
--     docker compose down -v
--     docker compose up
--
-- (The -v throws the old data away. Without it, this file will not re-run.)
-- ---------------------------------------------------------------------------

INSERT INTO products (name, description, price, image_file) VALUES
    ('Bamboo Water Bottle',
     'Holds 750ml and keeps it cold all afternoon. Made from fast-growing bamboo.',
     450.00,
     'bottle.svg'),

    ('Island Tote Bag',
     'Strong cotton tote for the market, the beach, or a very large sandwich.',
     320.00,
     'tote.svg'),

    ('Coconut Bowl Set',
     'Four bowls, each one polished from a single coconut shell. No two alike.',
     580.00,
     'bowls.svg'),

    ('Hand-Painted Notebook',
     'Eighty blank pages behind a cover painted by hand in Phuket Old Town.',
     180.00,
     'notebook.svg'),

    ('Woven Sun Hat',
     'Wide brim, light as anything, folds flat into your bag.',
     390.00,
     'hat.svg'),

    ('Beach Sandals',
     'Recycled rubber soles. Comfortable from the very first walk.',
     250.00,
     'sandals.svg');