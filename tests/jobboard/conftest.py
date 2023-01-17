import pytest

from jobboard.models import Company, Job


@pytest.fixture
def company(db):
    return Company.objects.create(name="Django Girls Foundation", logo="django_girls.png")


@pytest.fixture
def company2(db):
    return Company.objects.create(name="Django Software Foundation", logo="django.png")


@pytest.fixture
def job(db, company):
    return Job.objects.create(
        company=company,
        role="Software Engineer",
        location="Remote - EMEA",
        summary="We are looking for a Full Stack Engineer.",
        description="Details for the job include paid vacation and funded travel.",
        open=True,
        remuneration="",
        apply="https://test.com/software_engineer/",
    )


@pytest.fixture
def jobs(db, company, company2):
    jobs = Job.objects.bulk_create(
        [
            Job(
                company=company,
                role="Full Stack Software Engineer",
                location="Remote - EMEA",
                summary="We are looking for a Full Stack Engineer.",
                description="Details for the job include paid vacation and funded travel.",
                open=True,
                remuneration="",
                apply="https://test.com/software_engineer/",
            ),
            Job(
                company=company2,
                role="Python Backend Software Engineer",
                location="Remote - USA",
                summary="We are looking for a Python Backend Software Engineer.",
                description="Details for the job include paid vacation and funded travel.",
                open=True,
                remuneration="",
                apply="https://test.com/backend_software_engineer/",
            ),
            Job(
                company=company,
                role="DevOps Software Engineer",
                location="New York, USA",
                summary="We are looking for a DevOps Engineer.",
                description="Details for the job include paid vacation and funded travel.",
                open=True,
                remuneration="",
                apply="https://test.com/devops_engineer/",
            ),
            Job(
                company=company2,
                role="Site Reliability Engineering Systems Engineer",
                location="London, UK",
                summary="We are looking for a Site Reliability Engineering Systems  Engineer.",
                description="Details for the job include paid vacation and funded travel.",
                open=True,
                remuneration="",
                apply="https://test.com/systems_engineer/",
            ),
        ]
    )
    return jobs


@pytest.fixture
def new_job(company2):
    return {
        "company": company2,
        "rol": "Site Reliability Engineering Systems Engineer",
        "location": "London, UK",
        "summary": "We are looking for a Site Reliability Engineering Systems  Engineer.",
        "description": "Details for the job include paid vacation and funded travel.",
        "open": True,
        "remuneration": "",
        "apply": "https://test.com/sre_systems_engineer/",
    }


@pytest.fixture
def new_company():
    return {"name": "Canonical", "logo": "canonical.svg"}


@pytest.fixture
def edit_company():
    return {"name": "Django Girls Foundation", "logo": "django_girls_foundation_logo.png"}
