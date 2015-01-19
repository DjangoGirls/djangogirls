from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse

from .models import Job


def jobs(request):
    job_offers = Job.objects.filter(ready_to_publish=True).filter(expiration_date__gte=timezone.now())
    return render(
        request, 
        'jobs/jobs.html', 
        {
            'job_offers': job_offers
        }
    )

def job_details(request, id):
    queryset = Book.objects.filter(ready_to_publish=True).filter(expiration_date__gte=timezone.now())
    job = get_object_or_404(queryset, id=id)
    return TemplateResponse(
        request,
        'jobs/job_details.html',
        {
            'job': job,
        }
    )
