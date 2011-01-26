ALTER TABLE people_grant
    ADD COLUMN agency_id SMALLINT NOT NULL
    ADD CONSTRAINT people_agency FOREIGN KEY (agency_id) REFERENCES people_agency
;


ALTER TABLE people_grant_translation
    DROP COLUMN agency
;