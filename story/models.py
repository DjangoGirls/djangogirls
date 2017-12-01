from django.db import models


class Story(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=True)
    post_url = models.URLField(null=False, blank=False)
    image = models.ImageField(upload_to="stories/", null=True)
    created = models.DateField(auto_now_add=True, null=False, blank=False)
    # False means a regular blogpost, not a story
    is_story = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "story"
        verbose_name_plural = "stories"
