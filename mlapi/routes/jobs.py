from fastapi import APIRouter
from rq.job import Job
import json
from schemas.jobs import JobResponse, JobId
from utils.logger_config import get_logger
from redisStore.queue import get_redis_con

# API router for job-releated endpoints which defines the root path as /api/jobs
router = APIRouter(prefix="/api/jobs", tags=["jobs"]) 
logger = get_logger(__name__) # create logger instance with the name of current module


# GET /api/jobs/results/{job_id}
@router.get("/results/{job_id}", response_model=JobResponse)
async def get_job_results(job_id: str):
    """
    GET: Returns the results of a job.

    This endpoint fetches the results of a job from the Redis queue using the job_id.
    It checks the status of the job and returns the result if the job is finished.
    If the job is not found or not finished, it returns an appropriate message.

    Args:
        job_id (str): The unique identifier of the job.

    Returns:
        Response: A JSON response containing the job result if finished, or a message indicating the job status.
    """
    logger.info(f"Fetching results for job_id: {job_id}")
    conn = get_redis_con() # establish connection to Redis

    # Fetch the job from Redis using the provided job_id
    try:
        job = Job.fetch(job_id, connection=conn)
    except Exception as e:
        logger.warning(f"Job not found: {job_id}. Error: {str(e)}")
        return ({"message": "Job not found.", "status": "error"}), 404
    
    # Check if the job is finished
    if not job.is_finished:
        logger.info(f"Job is not finished yet: {job_id}")
        return {"message": "Job is not finished yet.", "status": "pending"}

    # If the job is finished, return the result
    try:
        result = job.result
        # Check if the result contains errors
        if "errors" in result:
            return ({"errors": result["errors"]}), 400
        json_string = json.dumps(result)
        logger.info(f"Job finished successfully: {job_id}")
        return {"result": json.loads(json_string), "status": "success"}
    except Exception as e:
        logger.error(f"Error processing job result for job_id {job_id}: {str(e)}")
        return (
            (
                {
                    "message": "Error processing job result",
                    "error": str(e),
                    "status": "error",
                }
            ),
            500,
        )
