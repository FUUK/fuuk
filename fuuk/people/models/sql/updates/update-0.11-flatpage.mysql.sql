INSERT INTO django_flatpage (id, url, title, title_en, title_cs, content, content_en, content_cs, enable_comments,
                             template_name, registration_required)
    SELECT f.id, f.url, coalesce(f_en.title, ''), f_en.title, f_cs.title, coalesce(f_en.content, ''), f_en.content,
        f_cs.content, f.enable_comments, f.template_name, f.registration_required
        FROM multilingual_flatpage AS f
            LEFT OUTER JOIN multilingual_flatpagetranslation AS f_en
                ON (f.id=f_en.master_id AND f_en.language_code='en')
            LEFT OUTER JOIN multilingual_flatpagetranslation AS f_cs
                ON (f.id=f_cs.master_id AND f_cs.language_code='cs');

INSERT INTO django_flatpage_sites (flatpage_id, site_id)
    SELECT flatpage_id, site_id FROM multilingual_flatpage_sites;
