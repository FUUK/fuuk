ALTER TABLE people_course ADD COLUMN name varchar(200);
ALTER TABLE people_course ADD COLUMN name_en varchar(200);
ALTER TABLE people_course ADD COLUMN name_cs varchar(200);
ALTER TABLE people_course ADD COLUMN annotation longtext;
ALTER TABLE people_course ADD COLUMN annotation_en longtext;
ALTER TABLE people_course ADD COLUMN annotation_cs longtext;
ALTER TABLE people_course ADD COLUMN note longtext;
ALTER TABLE people_course ADD COLUMN note_en longtext;
ALTER TABLE people_course ADD COLUMN note_cs longtext;

UPDATE people_course AS t1
    INNER JOIN people_coursetranslation AS t2
        ON t1.id=t2.master_id
    SET t1.name_en=t2.name,
        t1.annotation_en=t2.annotation,
        t1.note_en=t2.note WHERE t2.language_code='en';
UPDATE people_course AS t1
    INNER JOIN people_coursetranslation AS t2
        ON t1.id=t2.master_id
    SET t1.name_cs=t2.name,
        t1.annotation_cs=t2.annotation,
        t1.note_cs=t2.note WHERE t2.language_code='cs';

UPDATE people_course SET name=coalesce(name_en, '');
ALTER TABLE people_course MODIFY name varchar(200) NOT NULL;
