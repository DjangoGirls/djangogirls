from django.urls import reverse
from pytest_django.asserts import assertContains, assertQuerysetEqual, assertTemplateUsed

from jobboard.models import Job


def test_jobboard_index_view(client, jobs):
    response = client.get(reverse("jobboard:index"))
    assert response.status_code == 200
    job_list = Job.objects.filter(open=True).order_by("-date_created")
    assertContains(response, "Site Reliability Engineering Systems Engineer")
    assertTemplateUsed(response, "jobboard/index.html")
    assert len(job_list) == 4
    assertQuerysetEqual(list(response.context["job_list"]), job_list)


def test_job_detail_view(client, job):
    response = client.get(reverse("jobboard:job_detail", args=(job.id,)))
    assert response.status_code == 200
    assertContains(response, "Software Engineer")
    assertTemplateUsed(response, "jobboard/job.html")
