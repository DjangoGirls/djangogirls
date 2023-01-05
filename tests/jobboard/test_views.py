from django.urls import reverse

from pytest_django.asserts import assertContains, assertTemplateUsed


def test_jobboard_index_view(client, jobs):
    response = client.get(reverse('jobboard:index'))
    assert response.status_code == 200
    assertContains(response, 'Site Reliability Engineering Systems Engineer')
    assertTemplateUsed(response, 'jobboard/index.html')


def test_job_detail_view(client, job):
    response = client.get(reverse('jobboard:job_detail', args=(job.id,)))
    assert response.status_code == 200
    assertContains(response, "Software Engineer")
    assertTemplateUsed(response, 'jobboard/job.html')
