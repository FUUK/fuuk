ALTER TABLE people_grant
  ADD COLUMN agency_id integer REFERENCES people_agency (id) DEFERRABLE INITIALLY DEFERRED;

-- Migration is too difficult


ALTER TABLE people_grant
  ALTER COLUMN agency_id SET NOT NULL;

ALTER TABLE people_grant_translation
  DROP COLUMN agency;