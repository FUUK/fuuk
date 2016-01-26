ALTER TABLE people_agency ADD COLUMN shortcut varchar(10);
ALTER TABLE people_agency ADD COLUMN shortcut_en varchar(10);
ALTER TABLE people_agency ADD COLUMN shortcut_cs varchar(10);
ALTER TABLE people_agency ADD COLUMN name varchar(100);
ALTER TABLE people_agency ADD COLUMN name_en varchar(100);
ALTER TABLE people_agency ADD COLUMN name_cs varchar(100);

UPDATE people_agency AS t1
    INNER JOIN people_agencytranslation AS t2
        ON t1.id=t2.master_id
    SET t1.name_en=t2.name,
        t1.shortcut_en=t2.shortcut WHERE t2.language_code='en';
UPDATE people_agency AS t1
    INNER JOIN people_agencytranslation AS t2
        ON t1.id=t2.master_id
    SET t1.name_cs=t2.name,
        t1.shortcut_cs=t2.shortcut WHERE t2.language_code='cs';

UPDATE people_agency SET name=coalesce(name_en, ''), shortcut=coalesce(shortcut_en, '');
ALTER TABLE people_agency MODIFY name varchar(100) NOT NULL;
ALTER TABLE people_agency MODIFY shortcut varchar(10) NOT NULL;
