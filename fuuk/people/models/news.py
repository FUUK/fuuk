from django.db import models
from django.core.exceptions import ValidationError

import multilingual


class News(models.Model):
    start = models.DateField()
    end = models.DateField()
    hyperlink = models.URLField(
        max_length=255,
        blank=True, null=True,
        verify_exists=True,
        help_text='This hyperlink will be added to the news title. Fill in form of www.link.com'
    )

    class Translation(multilingual.Translation):
        title = models.CharField(max_length=255)
        content = models.TextField()

    class Meta:
        app_label = "people"
        ordering = ('end',)
        verbose_name_plural = "News"

    def __unicode__(self):
        return self.title or u""
    
    def clean(self):
        if self.start > self.end:
            raise ValidationError('The event cant end before it starts.')