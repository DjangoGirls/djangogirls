import pytest

from jobboard.models import Job


@pytest.fixture
def job(db, globalpartner):
    return Job.objects.create(
        company=globalpartner,
        role="Software Engineer",
        location="Remote - EMEA",
        summary="We are looking for a Full Stack Engineer.",
        description="Details for the job include paid vacation and funded travel.",
        open=True,
        remuneration="",
        apply="https://test.com/software_engineer/",
    )


@pytest.fixture
def jobs(db, globalpartner, globalpartner2):
    jobs = Job.objects.bulk_create(
        [
            Job(
                company=globalpartner,
                role="Full Stack Software Engineer",
                location="Remote - EMEA",
                summary="We are looking for a Full Stack Engineer.",
                description="Details for the job include paid vacation and funded travel.",
                open=True,
                remuneration="",
                apply="https://test.com/software_engineer/",
            ),
            Job(
                company=globalpartner2,
                role="Python Backend Software Engineer",
                location="Remote - USA",
                summary="We are looking for a Python Backend Software Engineer.",
                description="Details for the job include paid vacation and funded travel.",
                open=True,
                remuneration="",
                apply="https://test.com/backend_software_engineer/",
            ),
            Job(
                company=globalpartner,
                role="DevOps Software Engineer",
                location="New York, USA",
                summary="We are looking for a DevOps Engineer.",
                description="Details for the job include paid vacation and funded travel.",
                open=True,
                remuneration="",
                apply="https://test.com/devops_engineer/",
            ),
            Job(
                company=globalpartner2,
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
def new_job(globalpartner2):
    return {
        "company": globalpartner2,
        "rol": "Site Reliability Engineering Systems Engineer",
        "location": "London, UK",
        "summary": "We are looking for a Site Reliability Engineering Systems  Engineer.",
        "description": "Details for the job include paid vacation and funded travel.",
        "open": True,
        "remuneration": "",
        "apply": "https://test.com/sre_systems_engineer/",
    }
