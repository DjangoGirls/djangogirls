from django.views.generic.list import ListView

from story.models import Story


class StoryListView(ListView):
    context_object_name = "stories"
    template_name = "story/stories.html"
    queryset = Story.objects.filter(is_story=True).order_by("-created")
