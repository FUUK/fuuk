ALTER TABLE people_thesis ADD COLUMN title varchar(255);
ALTER TABLE people_thesis ADD COLUMN title_en varchar(255);
ALTER TABLE people_thesis ADD COLUMN title_cs varchar(255);
ALTER TABLE people_thesis ADD COLUMN annotation text;
ALTER TABLE people_thesis ADD COLUMN annotation_en text;
ALTER TABLE people_thesis ADD COLUMN annotation_cs text;
ALTER TABLE people_thesis ADD COLUMN abstract text;
ALTER TABLE people_thesis ADD COLUMN abstract_en text;
ALTER TABLE people_thesis ADD COLUMN abstract_cs text;
ALTER TABLE people_thesis ADD COLUMN keywords text;
ALTER TABLE people_thesis ADD COLUMN keywords_en text;
ALTER TABLE people_thesis ADD COLUMN keywords_cs text;

UPDATE people_thesis AS t1
    INNER JOIN people_thesistranslation AS t2
        ON t1.id=t2.master_id
    SET t1.title_en=t2.title,
        t1.annotation_en=t2.annotation,
        t1.abstract_en=t2.abstract,
        t1.keywords_en=t2.keywords WHERE t2.language_code='en';
UPDATE people_thesis AS t1
    INNER JOIN people_thesistranslation AS t2
        ON t1.id=t2.master_id
    SET t1.title_cs=t2.title,
        t1.annotation_cs=t2.annotation,
        t1.abstract_cs=t2.abstract,
        t1.keywords_cs=t2.keywords WHERE t2.language_code='cs';

UPDATE people_thesis SET title=coalesce(title_en, '');
ALTER TABLE people_thesis MODIFY  title varchar(255) NOT NULL;
