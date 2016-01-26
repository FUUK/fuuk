ALTER TABLE people_grant ADD COLUMN title varchar(200);
ALTER TABLE people_grant ADD COLUMN title_en varchar(200);
ALTER TABLE people_grant ADD COLUMN title_cs varchar(200);
ALTER TABLE people_grant ADD COLUMN annotation longtext;
ALTER TABLE people_grant ADD COLUMN annotation_en longtext;
ALTER TABLE people_grant ADD COLUMN annotation_cs longtext;

UPDATE people_grant AS t1
    INNER JOIN people_granttranslation AS t2
        ON t1.id=t2.master_id
    SET t1.title_en=t2.title,
        t1.annotation_en=t2.annotation WHERE t2.language_code='en';
UPDATE people_grant AS t1
    INNER JOIN people_granttranslation AS t2
        ON t1.id=t2.master_id
    SET t1.title_cs=t2.title,
        t1.annotation_cs=t2.annotation WHERE t2.language_code='cs';

UPDATE people_grant SET title=coalesce(title_en, '');
UPDATE people_grant SET annotation=coalesce(annotation_en, '');

ALTER TABLE people_grant MODIFY title varchar(200) NOT NULL;
ALTER TABLE people_grant MODIFY annotation longtext NOT NULL;
