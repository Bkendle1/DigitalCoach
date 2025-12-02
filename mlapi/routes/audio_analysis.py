from fastapi import APIRouter, HTTPException
from schemas.jobs import JobId, JobResponse, JobStatus
from schemas.create_answer import AudioSentimentResult
from redisStore.queue import add_task_to_queue
from tasks.assemblyai_api import detect_audio_sentiment
from rq.job import Job
from redisStore.myconnection import get_redis_con
from utils.logger_config import get_logger
from pydantic import BaseModel, Field, field_validator 
from rq.exceptions import NoSuchJobError

logger = get_logger(__name__)

router = APIRouter(prefix="/api/audio_analysis", tags=["analysis"])


class AudioAnalysisRequest(BaseModel):
    """
    Request to start an audio analysis job
    Args: 
        video_url: The URL of the video to analyze
    Returns:
        AudioAnalysisRequest: The request object
    Raises:
        ValueError: If the video_url is empty or not a valid URL
    """

    video_url: str = Field(...,description="URL to analyze")

    @field_validator("video_url")
    @classmethod
    def validate_url(cls, url: str):
        """
        Validate the video URL to ensure not empty or invalid
        Args:
            url: The URL or file path to validate
        Returns:
            url: The trimmed URL or path
        Raises:
            ValueError: If the URL is empty 
        """
        url = url.strip()
        if not url:
            raise ValueError("video_url cannot be empty")
        return url 
        
    

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


@router.get(
    "/{job_id}/result",
    response_model=AudioSentimentResult,
    summary="Get the result of a completed audio analysis job",
    description="Get the full result of a completed audio analysis job",
)
async def get_audio_analysis_result(job_id: str):
    """
    Get the result of a completed audio analysis job.

    Args: 
        job_id: The ID of the audio analysis job to get the status of
    Returns: 
        AudioSentimentResult: The complete audio analysis result
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
            logger.error(f"Job {job_id} failed with exception: {str(job.exc_info)}")
            raise HTTPException(status_code=500, detail=str(job.exc_info))

        # Check if the job is finished (success)
        if job.is_finished:
            result = job.result

            # Check if the result is an exception
            if isinstance(result, Exception):
                logger.error(f"Job {job_id} was completed with an exception: {str(result)}")
                raise HTTPException(status_code=500, detail=f"Job failed: {str(result)}")

            # Check if result is AudioSentimentResult type 
            if not isinstance(result, AudioSentimentResult):
                logger.warning(f"Job {job_id} result is not AudioSentimentResult type")
                # Try to convert if it's a dict
                if isinstance(result, dict):
                    result = AudioSentimentResult(**result)
                else:
                    raise HTTPException(status_code=500, detail="Job result is in an unexpected format, conversion has failed")

            logger.info(f"Result of audio analysis job {job_id} has been retrieved")
            return result

        # Check if job is still processing 
        if job.is_started:
            logger.info(f"Job {job_id} is still processing")
            raise HTTPException(status_code=202, detail="Job is still processing")

        # Job is still processing       
        logger.info(f"Job {job_id} has not started yet")
        raise HTTPException(status_code=202, detail="Job has not started yet")

    except NoSuchJobError:
        logger.warning(f"Trying to access non-existant job: {job_id}")
        raise HTTPException(status_code=404, detail="Job not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting audio analysis job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
        
