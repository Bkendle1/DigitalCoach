from fastapi import APIRouter, HTTPException, Depends
from redisStore.myconnection import get_redis_con
from utils.logger_config import get_logger
from schemas import StarFeedbackRequest, StarFeedbackResponse, JobId
from services import orchestrator, jobs
from redis import Redis

logger = get_logger(__name__)

router = APIRouter(prefix="/api/star_feedback", tags=["star_feedback"])

def get_redis():
    """
    Get Redis connection
    """
    return get_redis_con()

# POST /api/star_feedback/analyze
@router.post(
        "/analyze",
        response_model=JobId)
async def analyze_star_method(request: StarFeedbackRequest):
    """
    Analyze text using the STAR method (Situation, Task, Action, Result)

    The STAR method is a structured way to respond to behavioral interview questions,
    which helps candidates provide concrete examples of their skills and experiences.

    This endpoint analyzes text to determine how well it follows the STAR structure
    and provides feedback on improving the response.

    Returns a job ID that can be used to track the status of the analysis.
    The results will be processed by success or failure handlers.

    Args:
        request (StarFeedbackRequest): Request model containing the text to analyze
    Returns:
    """
    try:
        # Check that the input text is long enough for analysis
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Text is too short for analysis. Please provide a more detailed response.",
            )

        # Trigger STAR analysis task
        job_id = orchestrator.start_star_feedback_analysis(request.text) 
        
        return JobId(job_id=job_id)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing STAR method: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze text using STAR method: {str(e)}",
        )


# GET /api/star_feedback/{job_id}
@router.get(
        "/{job_id}",
        response_model=StarFeedbackResponse,
        summary="Get the result of a STAR feedback analysis job",
        description="Retrieve the results of a completed STAR feedback analysis job using the job ID",
        )
async def get_star_feedback_result(job_id: str, redis : Redis=Depends(get_redis)):
    """
    Get the result of a completed STAR feedback analysis job.

    Only returns the result if the job is completed, otherwise raises an error.
    """
    logger.info(f"Fetching results for job_id: {job_id}")
    # # get connection
    # conn = get_redis_con()

    try:
        job_status_data = jobs.get_job_status(job_id, redis)
        if job_status_data is None:
            logger.warning(f"Job not found: {job_id}")
            return HTTPException(status_code=404, detail=f"Job not found: {job_id}")
        # job = Job.fetch(job_id, connection=redis)
    except Exception as e:
        logger.warning(f"Job not found: {job_id}. Error: {str(e)}")
        return HTTPException(status_code=404, detail=f"Job not found: {str(e)}")
    if not job.is_finished:
        logger.info(f"Job is not finished yet: {job_id}")
        return HTTPException(status_code=202, detail="Job is still processing")
    try:
        result = job.result
        if "errors" in result:
            return HTTPException(status_code=400, detail=result["errors"])
        json_string = json.dumps(result)
        logger.info(f"Job finished successfully: {job_id}")
        return {"result": json.loads(json_string), "status": "success"}
    except Exception as e:
        logger.error(f"Error processing job result for job_id {job_id}: {str(e)}")
        return HTTPException(
            status_code=500, detail=f"Error processing job result: {str(e)}"
        )
