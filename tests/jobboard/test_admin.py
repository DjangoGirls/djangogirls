from django.urls import reverse


def test_view_jobs_superuser(admin_client, jobs):
    response = admin_client.get(reverse("admin:jobboard_job_changelist"))
    assert response.status_code == 200


def test_edit_job_superuser(admin_client, job, new_job):
    response = admin_client.get(reverse("admin:jobboard_job_change", args=(job.pk,)))
    assert response.status_code == 200
    response = admin_client.post(reverse("admin:jobboard_job_change", args=(job.pk,)), data=new_job)
    assert response.status_code == 200


def test_add_job_superuser(admin_client, new_job):
    response = admin_client.get(reverse("admin:jobboard_job_add"))
    assert response.status_code == 200
    response = admin_client.post(reverse("admin:jobboard_job_add"), data=new_job)
    assert response.status_code == 200


def test_view_companies_superuser(admin_client):
    response = admin_client.get(reverse("admin:jobboard_company_changelist"))
    assert response.status_code == 200


def test_add_new_company_superuser(admin_client, new_company):
    response = admin_client.get(reverse("admin:jobboard_company_add"))
    assert response.status_code == 200
    response = admin_client.post(reverse("admin:jobboard_company_add"), data=new_company)
    assert response.status_code == 200


def test_edit_company_superuser(admin_client, company, edit_company):
    response = admin_client.get(reverse("admin:jobboard_company_change", args=(company.pk,)))
    assert response.status_code == 200
    response = admin_client.post(reverse("admin:jobboard_company_change", args=(company.pk,)), data=edit_company)
    assert response.status_code == 200


"""Tests to make sure only superusers can manage companies and jobs and organizers have no
access to this module."""


def test_add_job_organizer(user_client, new_job):
    response = user_client.get(reverse("admin:jobboard_job_add"))
    assert response.status_code == 302


def test_view_jobs_organizer(user_client):
    response = user_client.get(reverse("admin:jobboard_job_changelist"))
    assert response.status_code == 302


def test_edit_job_organizer(user_client, job):
    response = user_client.get(reverse("admin:jobboard_job_change", args=(job.pk,)))
    assert response.status_code == 302


def test_view_companies_organizer(user_client):
    response = user_client.get(reverse("admin:jobboard_company_changelist"))
    assert response.status_code == 302


def test_add_company_organizer(user_client, new_company):
    response = user_client.get(reverse("admin:jobboard_company_add"))
    assert response.status_code == 302
    response = user_client.post(reverse("admin:jobboard_company_add"), data=new_company)
    assert response.status_code == 302


def test_edit_company_organizer(user_client, company, edit_company):
    response = user_client.get(reverse("admin:jobboard_company_change", args=(company.pk,)))
    assert response.status_code == 302
    response = user_client.post(reverse("admin:jobboard_company_change", args=(company.pk,)), data=edit_company)
    assert response.status_code == 302
