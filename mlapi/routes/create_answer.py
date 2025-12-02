from fastapi import APIRouter, HTTPException, Depends
from schemas import JobId, JobResponse, CreateAnswerJobRequest, CreateAnswerJobResponse
from services import orchestrator, jobs
from redisStore.myconnection import get_redis_con
from redis import Redis
from utils.logger_config import get_logger

logger = get_logger(__name__) # create a logger instance to log messages 

router = APIRouter(prefix="/api/create_answer", tags=["analysis"])

def get_redis():
    """
    Returns a Redis connnection instance.
    """
    return get_redis_con()

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

    Starts interview analysis consisting of an audio analysis job followed by a create_answer job
    
    Args:
        request (CreateAnswerJobRequest): The request body containing the video URL.
    Returns:
        JobId: The ID of the created job.
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
    response_model=CreateAnswerJobResponse,
    summary="Get the status of a create_answer job",
    description="Check the status of a create_answer job",
)
async def get_answer_job(job_id: str, redis: Redis = Depends(get_redis)):
    """
    Get the status of a create_answer job with the given job ID.

    Args:
        job_id (str):  The ID of the job to check.
        redis (Redis): The Redis connection instance, injected by FastAPI's Depends which can be replaced with a fake Redis object during testing.
    Returns:
        Returns the job status in the form of JobResponse schema.
    """

    try:
        
        # Get the job status from Redis
        job_status_data = jobs.get_job_status(job_id, redis)
        
        # Handle job not found
        if not job_status_data:
            logger.warning(f"Job {job_id} not found.")
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found.")

        return job_status_data
    # Catch HTTP exceptions and re-raise them
    except HTTPException: 
        raise
    # Catch all other exceptions
    except Exception as e:
        logger.error(f"System error fetching job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")