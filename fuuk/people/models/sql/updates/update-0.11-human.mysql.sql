ALTER TABLE people_human ADD COLUMN subtitle varchar(200);
ALTER TABLE people_human ADD COLUMN subtitle_en varchar(200);
ALTER TABLE people_human ADD COLUMN subtitle_cs varchar(200);
ALTER TABLE people_human ADD COLUMN cv longtext;
ALTER TABLE people_human ADD COLUMN cv_en longtext;
ALTER TABLE people_human ADD COLUMN cv_cs longtext;
ALTER TABLE people_human ADD COLUMN interests longtext;
ALTER TABLE people_human ADD COLUMN interests_en longtext;
ALTER TABLE people_human ADD COLUMN interests_cs longtext;
ALTER TABLE people_human ADD COLUMN stays longtext;
ALTER TABLE people_human ADD COLUMN stays_en longtext;
ALTER TABLE people_human ADD COLUMN stays_cs longtext;

UPDATE people_human AS t1
    INNER JOIN people_humantranslation AS t2
        ON t1.id=t2.master_id
    SET t1.subtitle_en=t2.subtitle,
        t1.cv_en=t2.cv,
        t1.interests_en=t2.interests,
        t1.stays_en=t2.stays WHERE t2.language_code='en';
UPDATE people_human AS t1
    INNER JOIN people_humantranslation AS t2
        ON t1.id=t2.master_id
    SET t1.subtitle_cs=t2.subtitle,
        t1.cv_cs=t2.cv,
        t1.interests_cs=t2.interests,
        t1.stays_cs=t2.stays WHERE t2.language_code='cs';
