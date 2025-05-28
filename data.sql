BEGIN;

-- Reset des tables
DELETE FROM exchange_exchange;
DELETE FROM favorite_favorite;
DELETE FROM puzzle_puzzle;
DELETE FROM city_city;
DELETE FROM brand_brand;
DELETE FROM category_category;

-- Reset des séquences
ALTER SEQUENCE brand_brand_id_seq RESTART WITH 1;
ALTER SEQUENCE category_category_id_seq RESTART WITH 1;
ALTER SEQUENCE city_city_id_seq RESTART WITH 1;
ALTER SEQUENCE puzzle_puzzle_id_seq RESTART WITH 1;
ALTER SEQUENCE favorite_favorite_id_seq RESTART WITH 1;
ALTER SEQUENCE exchange_exchange_id_seq RESTART WITH 1;

-- Insertion des marques
INSERT INTO brand_brand (id, name) VALUES
    (1, 'Ravensburger'),
    (2, 'Clementoni'),
    (3, 'Educa');

-- Insertion des catégories (7 total)
INSERT INTO category_category (id, name) VALUES
    (1, 'Nature'),
    (2, 'Art'),
    (3, 'Animaux'),
    (4, 'Architecture'),
    (5, 'Voyage'),
    (6, 'Fantaisie'),
    (7, 'Historique');

-- Insertion des villes
INSERT INTO city_city (id, name, zip_code, country) VALUES
    (1, 'Paris', '75000', 'france'),
    (2, 'Lyon', '69000', 'france');

-- Génération de 500 puzzles
DO $$
DECLARE
    i INT;
    owner_ids INT[] := ARRAY[2,3,6,7,9,10,11,12,13,14];
    brand_ids INT[] := ARRAY[1,2,3];
    category_ids INT[] := ARRAY[1,2,3,4,5,6,7];
    owner_id INT;
BEGIN
    FOR i IN 1..500 LOOP
        owner_id := owner_ids[(i % array_length(owner_ids, 1)) + 1];
        INSERT INTO puzzle_puzzle (
            name, piece_count, description, condition, status, is_published,
            created, brand_id, category_id, owner_id, image
        )
        VALUES (
            'Puzzle #' || i,
            500 + (random() * 1000)::int,
            'Description pour le puzzle #' || i,
            CASE WHEN random() > 0.5 THEN 'new' ELSE 'used' END,
            CASE 
                WHEN random() < 0.7 THEN 'available' 
                ELSE 'swap' 
            END,
            TRUE,
            NOW(),
            brand_ids[(random() * 2 + 1)::int],
            category_ids[(random() * 6 + 1)::int],
            owner_id,
            'puzzle_images/puzzle_' || i || '.jpg'
        );
    END LOOP;
END $$;

-- Génération de 300 favoris (pas d'auto-favoris)
WITH all_puzzles AS (
    SELECT id, owner_id FROM puzzle_puzzle
),
eligible_favorites AS (
    SELECT p.id AS puzzle_id, u.id AS user_id
    FROM all_puzzles p, unnest(ARRAY[2,3,6,7,9,10,11,12,13,14]) u(id)
    WHERE p.owner_id != u.id
    ORDER BY random()
    LIMIT 300
)
INSERT INTO favorite_favorite (created, puzzle_id, owner_id)
SELECT NOW(), puzzle_id, user_id
FROM eligible_favorites;

-- Génération de 100 échanges valides
WITH user_puzzles AS (
    SELECT id AS puzzle_id, owner_id
    FROM puzzle_puzzle
),
requester_proposals AS (
    SELECT puzzle_id AS proposed_id, owner_id AS requester_id
    FROM user_puzzles
),
asked_candidates AS (
    SELECT puzzle_id AS asked_id, owner_id AS owner_id
    FROM user_puzzles
),
valid_exchange_candidates AS (
    SELECT DISTINCT ON (rp.proposed_id)
        NOW() AS created,
        NOW() AS updated,
        ac.owner_id AS owner_id,
        rp.requester_id AS requester_id,
        ac.asked_id AS puzzle_asked_id,
        rp.proposed_id AS puzzle_proposed_id,
        CASE 
            WHEN random() < 0.6 THEN 'pending'
            WHEN random() < 0.85 THEN 'accepted'
            ELSE 'denied'
        END AS status
    FROM requester_proposals rp
    JOIN asked_candidates ac 
        ON rp.requester_id != ac.owner_id
    WHERE rp.proposed_id != ac.asked_id
    ORDER BY rp.proposed_id, random()
    LIMIT 100
)
INSERT INTO exchange_exchange (
    status, created, updated, owner_id, requester_id, puzzle_asked_id, puzzle_proposed_id
)
SELECT 
    status, created, updated, owner_id, requester_id, puzzle_asked_id, puzzle_proposed_id
FROM valid_exchange_candidates;

COMMIT;
