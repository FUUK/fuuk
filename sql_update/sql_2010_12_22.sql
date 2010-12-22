ALTER TABLE people_article
  ALTER COLUMN identification TYPE character varying(100),
  ALTER COLUMN publication TYPE character varying(100)
;

ALTER TABLE people_place
  ALTER COLUMN department_id DROP NOT NULL
;
