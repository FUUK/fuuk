ALTER TABLE people_place ADD COLUMN name varchar(200);
ALTER TABLE people_place ADD COLUMN name_en varchar(200);
ALTER TABLE people_place ADD COLUMN name_cs varchar(200);

UPDATE people_place AS t1
    INNER JOIN people_placetranslation AS t2
        ON t1.id = t2.master_id
    SET t1.name_en=t2.name WHERE t2.language_code='en';
UPDATE people_place AS t1
    INNER JOIN people_placetranslation AS t2
        ON t1.id = t2.master_id
    SET t1.name_cs=t2.name WHERE t2.language_code='cs';

UPDATE people_place SET name=coalesce(name_en, '');
ALTER TABLE people_place MODIFY name varchar(200) NOT NULL;
