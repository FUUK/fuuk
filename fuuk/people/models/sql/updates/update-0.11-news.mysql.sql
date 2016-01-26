ALTER TABLE people_news ADD COLUMN title varchar(255);
ALTER TABLE people_news ADD COLUMN title_en varchar(255);
ALTER TABLE people_news ADD COLUMN title_cs varchar(255);
ALTER TABLE people_news ADD COLUMN content longtext;
ALTER TABLE people_news ADD COLUMN content_en longtext;
ALTER TABLE people_news ADD COLUMN content_cs longtext;

UPDATE people_news AS t1
    INNER JOIN people_newstranslation AS t2
        ON t1.id = t2.master_id
    SET t1.title_en=t2.title,
        t1.content_en=t2.content WHERE t2.language_code='en';
UPDATE people_news AS t1
    INNER JOIN people_newstranslation AS t2
        ON t1.id = t2.master_id
    SET t1.title_cs=t2.title,
        t1.content_cs=t2.content WHERE t2.language_code='cs';

UPDATE people_news SET title=coalesce(title_en, ''), content=coalesce(content_en, '');
ALTER TABLE people_news MODIFY title varchar(255) NOT NULL;
ALTER TABLE people_news MODIFY content longtext NOT NULL;
