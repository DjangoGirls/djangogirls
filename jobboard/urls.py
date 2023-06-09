from django.urls import path

from . import views

app_name = "jobboard"


urlpatterns = [
    path("", views.index, name="index"),
    path("job/<int:id>/", views.job_detail, name="job_detail"),
]
