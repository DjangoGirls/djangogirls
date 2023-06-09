from django.db import models
from django.utils.translation import gettext_lazy as _


class Story(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(null=True)
    post_url = models.URLField()
    image = models.ImageField(upload_to="stories/", null=True)
    created = models.DateField(auto_now_add=True)
    # False means a regular blogpost, not a story
    is_story = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.post_url

    class Meta:
        verbose_name = _("story")
        verbose_name_plural = _("stories")
