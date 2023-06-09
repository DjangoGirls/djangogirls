def test_job_model_string_representation(job):
    assert str(job) == f"{job.company} - {job.role}"
