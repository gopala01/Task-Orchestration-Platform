from orchestrator.models import Job, JobState
from typing import Optional

_jobs = {}

def create_job(job_id: str) -> Job:
    job = Job(
        job_id=job_id,
        state=JobState.SUBMITTED,
        created_at=Job.now(),
        updated_at=Job.now(),
    )
    _jobs[job_id] = job
    return job

def get_job(job_id: str) -> Optional[Job]:
    return _jobs.get(job_id)

def update_state(job_id: str, new_state: JobState, error: Optional[str] = None):
    job = _jobs.get(job_id)
    if not job:
        return
    job.state = new_state
    job.updated_at = Job.now()
    job.error = error

def increment_attempt(job_id: str):
    job = _jobs.get(job_id)
    if job:
        job.attempt += 1

def cancel_job(job_id: str) -> bool:
    job = _jobs.get(job_id)
    if not job:
        return False
    if job.state in {JobState.COMPLETED, JobState.FAILED}:
        return False
    job.state = JobState.CANCELLED
    return True