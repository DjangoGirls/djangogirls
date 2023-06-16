from django.shortcuts import render

from .models import Job


def index(request):
    job_list = Job.objects.filter(open=True).order_by("-date_created")
    return render(request, "jobboard/index.html", {"job_list": job_list})


def job_detail(request, id):
    try:
        job = Job.objects.get(id=id)
    except Job.DoesNotExist:
        job = None

    return render(request, "jobboard/job.html", {"job": job})
