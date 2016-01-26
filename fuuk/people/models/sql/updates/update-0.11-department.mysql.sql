ALTER TABLE people_department ADD COLUMN name varchar(200);
ALTER TABLE people_department ADD COLUMN name_en varchar(200);
ALTER TABLE people_department ADD COLUMN name_cs varchar(200);

UPDATE people_department AS t1
    INNER JOIN people_departmenttranslation AS t2
        ON t2.id = t2.master_id
    SET t1.name_en = t2.name WHERE t2.language_code='en';
UPDATE people_department AS t1
    INNER JOIN people_departmenttranslation AS t2
        ON t2.id = t2.master_id
    SET t1.name_cs = t2.name WHERE t2.language_code='cs';

UPDATE people_department SET name=coalesce(name_en, '');
ALTER TABLE people_department MODIFY name varchar(200) NOT NULL;
