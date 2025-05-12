BEGIN;

DELETE FROM exchange_exchange;
DELETE FROM favorite_favorite;
DELETE FROM puzzle_puzzle;
DELETE FROM city_city;
DELETE FROM brand_brand;
DELETE FROM category_category;

ALTER SEQUENCE brand_brand_id_seq RESTART WITH 1;
ALTER SEQUENCE category_category_id_seq RESTART WITH 1;
ALTER SEQUENCE city_city_id_seq RESTART WITH 1;
ALTER SEQUENCE puzzle_puzzle_id_seq RESTART WITH 1;
ALTER SEQUENCE favorite_favorite_id_seq RESTART WITH 1;
ALTER SEQUENCE exchange_exchange_id_seq RESTART WITH 1;

COMMIT;

INSERT INTO brand_brand (id, name) VALUES
    (1, 'Ravensburger'),
    (2, 'Clementoni'),
    (3, 'Educa');

INSERT INTO category_category (id, name) VALUES
    (1, 'Nature'),
    (2, 'Art'),
    (3, 'Animaux');

INSERT INTO city_city (id, name, zip_code, country) VALUES
    (1, 'Paris', '75000', 'france'),
    (2, 'Lyon', '69000', 'france');

INSERT INTO puzzle_puzzle (
    id, name, piece_count, description, condition, status, is_published,
    created, brand_id, category_id, owner_id, image
)
VALUES
    (1, 'Montagne enneigée', 1000, 'Puzzle hivernal très relaxant.', 'new', 'available', TRUE, NOW(), 1, 1, 3, 'puzzle_images/montagne_enneigee.jpg'),
    (2, 'Le Cri - Munch', 500, 'Reproduction du célèbre tableau.', 'used', 'available', TRUE, NOW(), 2, 2, 6, 'puzzle_images/le_cri_munch.jpg'),
    (3, 'Chats rigolos', 750, 'Puzzle amusant avec des chats en costume.', 'used', 'swap', TRUE, NOW(), 3, 3, 7, 'puzzle_images/chats_rigolos.jpg'),
    (4, 'Plage au coucher du soleil', 1000, 'Très belle scène tropicale.', 'new', 'available', TRUE, NOW(), 1, 1, 6, 'puzzle_images/plage_coucher_soleil.jpg');

INSERT INTO favorite_favorite (id, created, puzzle_id, owner_id) VALUES
    (1, NOW(), 1, 6),
    (2, NOW(), 2, 3),
    (3, NOW(), 3, 3),
    (4, NOW(), 4, 7);

INSERT INTO exchange_exchange (
    id, status, created, updated, owner_id, requester_id,
    puzzle_asked_id, puzzle_proposed_id
)
VALUES
    (1, 'pending', NOW(), NOW(), 6, 3, 2, 1),
    (2, 'accepted', NOW(), NOW(), 3, 7, 1, 3),
    (3, 'denied', NOW(), NOW(), 7, 6, 3, 4);
