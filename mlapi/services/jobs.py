from rq.job import Job
from rq.exceptions import NoSuchJobError
from redis import Redis
from typing import Dict, Any
from schemas import JobResponse, JobStatus
from fastapi import HTTPException

def get_job_status(job_id: str, redis_conn: Redis) -> JobResponse:
    """
    Get the status of a job with the given job ID in the format of the JobResponse schema.
    
    Args:
        job_id (str): ID of the job to check
        redis_conn (Redis): Redis connection object
    Returns:
        Response (JobResponse): A dictionary containing the job status and result or error information in the format of the JobResponse schema.
    """ 

    # Attempt to get job object with given job ID
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except NoSuchJobError:
        return None
    
    # Initialize job status response based on JobResponse schema
    response = JobResponse(
        job_id = job_id,
        status=JobStatus.PENDING, # assume job is still in the queue
        result=None, 
        error=None)    

    # check job status
    # job failed, return failed status and error information
    if job.is_failed:
        response["status"] = JobStatus.FAILED,
        response["error"] = str(job.exc_info)
    # job finished, return complete status and result
    elif job.is_finished:
        response["status"] = JobStatus.COMPLETED,
        response["result"] = job.result,
    # job still processing, return processing status
    elif job.is_started:
        response["status"] = JobStatus.PROCESSING
    
    return response
