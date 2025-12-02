from fastapi import APIRouter, HTTPException
from schemas import JobId, JobResponse, CreateAnswerJobRequest, CreateAnswer
from redisStore.queue import add_task_to_queue
from services import orchestrator
# from tasks.create_answer_task import (
#     create_answer,
#     start_audio_analysis_job,
# )
from rq.job import Job
from redisStore.myconnection import get_redis_con
from utils.logger_config import get_logger

logger = get_logger(__name__) # create a logger instance to log messages 

router = APIRouter(prefix="/api/create_answer", tags=["analysis"])

# POST /api/create_answer
@router.post(
    "/",
    response_model=JobId,
    summary="Start an answer generation job for the given video",
    description="Starts a background job to analyze a video and generate an answer",
)
async def create_answer_job(request: CreateAnswerJobRequest):
    """
    Start a job to generate an answer for the given video URL.

    This will:
    1. Start an audio analysis job
    1. Start an audio analysis job using AssemblyAI
    3. Start a create_answer job that depends on the first two jobs
    """

    video_url = str(request.video_url) # convert video url into string
    logger.info(f"Received analysis request for: {video_url}")
    try:
        
        # Start the interview analysis job (currently only does audio analysis)
        job_id = orchestrator.start_interview_analysis(video_url)

        logger.info(f"Started create_answer job: {job_id}")

        return JobId(job_id=job_id) # return the job ID of the created job
    
    except Exception as e:
        # log any errors
        logger.error(f"Error starting create_answer job: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting create_answer job: {str(e)}")

# GET /api/create_answer/{job_id}
@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get the status of a create_answer job",
    description="Check the status of a create_answer job",
)
async def get_create_answer_job(job_id: str):
    """
    Get the status of a create_answer job with the given job ID.

    Returns the job status and result if available.
    """

    # Attempts to get the job object associated with the given job ID from Redis
    try:
        job = Job.fetch(job_id, connection=get_redis_con())

        # Check job status and return appropriate response
        if job.is_finished:
            result = job.result
            # If the result is an exception object, return the error with failed status
            if isinstance(result, Exception):
                return {
                    "job_id": job_id,
                    "status": "failed",
                    "error": str(result),
                }
            # Otherwise, return successful result
            return {
                "job_id": job_id,
                "status": "completed",
                "result": result.dict() if hasattr(result, "dict") else result,
            }
        # If the job has failed then return the error information
        elif job.is_failed:
            return {
                "job_id": job_id,
                "status": "failed",
                "error": str(job.exc_info),
            }
        # If the job is still being processed, return processing status
        elif job.is_started:
            return {
                "job_id": job_id,
                "status": "processing",
            }
        # If the job is queued or in any other state, return pending status
        else:
            return {
                "job_id": job_id,
                "status": "pending",
            }
    # Failed to fetch the job from Redis, likely because of invalid job ID
    except Exception as e:
        logger.error(f"Error getting create_answer job {job_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Job not found: {str(e)}")

# GET /api/create_answer/{job_id}/result
@router.get(
    "/{job_id}/result",
    response_model=CreateAnswer,
    summary="Get the result of a completed create_answer job",
    description="Get the full result of a completed create_answer job",
)
async def get_create_answer_result(job_id: str):
    """
    Get the result of a completed create_answer job.

    Only returns the result if the job is completed, otherwise raises an error.
    """
    # Attempt to fetch job object associated with the given job ID from Redis
    try:
        job = Job.fetch(job_id, connection=get_redis_con())

        # If the job is done, return the appropriate response
        if job.is_finished:
            result = job.result
            # If the result is an exception object, return the error details
            if isinstance(result, Exception):
                raise HTTPException(status_code=500, detail=str(result))
            # Otherwise, return the result
            return result
    
        # If the job failed, return error message
        elif job.is_failed:
            raise HTTPException(status_code=500, detail=str(job.exc_info))
        # If the job is in any other state, e.g. in queue or processing, return error
        else:
            raise HTTPException(status_code=202, detail="Job is still processing")
    # Failed to fetch job, likely due to invalid job ID
    except Exception as e:
        logger.error(f"Error getting create_answer result {job_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Job not found: {str(e)}")
