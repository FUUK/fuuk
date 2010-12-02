-- remove department and floor column
ALTER TABLE people_place_translation
    DROP COLUMN floor
;

-- add flag defended to thesis
ALTER TABLE people_thesis
    ADD COLUMN defended boolean
;
UPDATE people_thesis SET defended = false;
ALTER TABLE people_thesis ALTER COLUMN defended SET NOT NULL;

-- move some data from person to human
DROP TABLE people_person_translation;

ALTER TABLE people_human
    ADD COLUMN birth_date date,
    ADD COLUMN birth_place character varying (200),
    ADD COLUMN email character varying (200),
    ADD COLUMN photo character varying (200)
;
UPDATE people_human
    SET birth_date = pp.birth_date,
        birth_place = pp.birth_place,
        email = pp.email,
        photo = pp.photo
    FROM people_person pp
    WHERE people_human.id = pp.human_id
;
ALTER TABLE people_person
    DROP COLUMN birth_date,
    DROP COLUMN birth_place,
    DROP COLUMN email,
    DROP COLUMN photo,
    ADD COLUMN is_active boolean DEFAULT true NOT NULL
;

ALTER TABLE people_person
    ALTER COLUMN is_active DROP DEFAULT
;