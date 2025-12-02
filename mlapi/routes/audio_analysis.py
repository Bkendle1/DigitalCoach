from fastapi import APIRouter, HTTPException
from schemas import JobId, JobResponse, JobStatus, AudioSentimentResult, AudioAnalysisRequest
from redisStore.queue import add_task_to_queue
from tasks.assemblyai_api import detect_audio_sentiment
from rq.job import Job
from redisStore.myconnection import get_redis_con
from utils.logger_config import get_logger
from pydantic import BaseModel, Field, field_validator 
from rq.exceptions import NoSuchJobError

logger = get_logger(__name__)

router = APIRouter(prefix="/api/audio_analysis", tags=["analysis"])       
    

@router.post(
    "/",
    response_model=JobId,
    summary="Start an audio analysis job for the given video",
    description="Starts a background job to analyze audio using AssemblyAI",
)
async def start_audio_analysis_job(request: AudioAnalysisRequest) -> JobId:
    """
    Start a job to analyze audio from the video URL using AssemblyAI.

    This will extract audio and send it to AssemblyAI for:
    - Transcription
    - Sentiment analysis
    - Auto-highlights (key phrases)
    - Topic detection (IAB categories)

    Args:
        request: The AudioAnalysisRequest object that contains the video_url for analysis
    Returns:
        JobId: The job ID of the started job
    Raises:
        HTTPException: If the job cannot be started
    """
    try:
        # Use default video URL for testing if not provided
        # if not request.video_url:
        #     video_url = "https://assembly.ai/wildfires.mp3"
        
        # The actual video URL to analyze
        video_url = request.video_url
    
        logger.info(f"Started audio analysis job for URL: {video_url}")
        
        # Queue the audio analysis job
        job = add_task_to_queue(detect_audio_sentiment, video_url)
        job_id = job.get_id()
        
        logger.info(f"Successfully started audio analysis job: {job_id}")
        return JobId(job_id=job_id)

    except ValueError as e:
        logger.error(f"Validation error starting audio analysis job: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error starting audio analysis job: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    summary="Get the status of an audio analysis job",
    description="Check the status of a previously started audio analysis job"
)
async def get_audio_analysis_job(job_id: str) -> JobResponse:
    """
    Get the status of an audio analysis job.

    Args:
        job_id: The ID of the audio analysis job to get the status of
    Returns:
        JobResponse: The job status and result if available.
    Raises:
        HTTPException: If the job cannot be found or an error occurs
    """
    try:
        
        if not job_id or job_id.strip():
            raise HTTPException(status_code=400, detail="job_id cannot be empty")
        
        job_id = job_id.strip()
        job = Job.fetch(job_id, connection=get_redis_con())

        # Check if the job is failed (error)
        if job.is_failed:
            logger.warning(f"Job {job_id} failed with exception: {str(job.exc_info)}")
            return JobResponse(
                job_id=job_id,
                status=JobStatus.FAILED,
                error=str(job.exc_info),
            )

        # Check if the job is finished (success)
        if job.is_finished:
            result = job.result

            # Check if the result is an exception
            if isinstance(result, Exception):
                logger.warning(f"Job {job_id} was completed with an exception: {str(result)}")
                return JobResponse(
                    job_id=job_id,
                    status=JobStatus.FAILED,
                    error=str(result),
                )

            # Convert the result to a dictionary if it is a modern Pydantic model 
            result_dict = None
            if hasattr(result, "model_dump"): # Modern Pydantic models
                result_dict = result.model_dump()
            elif hasattr(result, "dict"): # Old Pydantic models
                result_dict = result.dict()
            elif isinstance(result, dict): # Dictionary
                result_dict = result
            else:
                # If result is not a modern Pydantic model, old Pydantic model, or dictionary
                logger.warning(f"Job {job_id} returned an unexpected result type: {type(result)}")
                raise HTTPException(status_code=500, detail="Unexpected result type")

            logger.info(f"Job {job_id} completed successfully")
            return JobResponse(
                job_id=job_id,
                status=JobStatus.COMPLETED,
                result=result_dict,
            )

        # Check if the job is still processing
        if job.is_started:
            logger.info(f"Job {job_id} is still processing")
            return JobResponse(
                job_id=job_id,
                status=JobStatus.PROCESSING,
            )
        # Check if the job is pending (not started)
        
        logger.info(f"Job {job_id} has not started yet")
        return JobResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
        )
    except NoSuchJobError:
        logger.warning(f"Trying to access non-existent job: {job_id}")
        raise HTTPException(status_code=404, detail="Job not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting audio analysis job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
