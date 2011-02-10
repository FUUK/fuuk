from django.db import models

import multilingual

class News(models.Model):
    start = models.DateField()
    end = models.DateField()
    hyperlink = models.CharField(max_length=255, blank=True, null=True, help_text='This hyperlink will be added to the news title. Fill in form of www.link.com')
          
    class Translation(multilingual.Translation):
        title = models.CharField(max_length=255)
        content = models.TextField()
        
    class Meta:
        app_label = "people"
        verbose_name_plural = "News"
        ordering = ['end']
        
    def __unicode__(self):
        return "%s" % (self.title)