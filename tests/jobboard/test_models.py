def test_company_model_string_representation(company):
    assert str(company) == company.name


def test_job_model_string_representation(job):
    assert str(job) == f'{job.company} - {job.role}'
