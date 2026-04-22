# Handles orchestration of tasks for interview videos, e.g. starting analysis jobs. 
# Can be called by route handlers.

from tasks.audio_analysis import detect_audio_sentiment
from redisStore.queue import add_task_to_queue
from tasks.create_answer_task import create_answer
from tasks.starscores import predict_star_scores
from tasks.feedback import analyze_interview_feedback
from utils.logger_config import get_logger
from schemas import (
    SentimentAnalysisRequest,
    AnalyzeInterviewRequest
)

logger = get_logger(__name__)

def start_audio_analysis(req: SentimentAnalysisRequest) -> str:
    """
    Start the audio analysis job by adding it to the queue.
    
    Args:
        req (SentimentAnalysisRequest): the request body of the audio analysis job which is currently just sentiment analysis.
    Returns:
        job_id (str): The Redis Job id of the queued audio analysis job.
    """
    logger.info(f"Started audio analysis job for interview={req.interview_id}.")
    
    # Enqueue sentiment analysis job
    # only pass the fields instead of the pydantic model
    job = add_task_to_queue("high", detect_audio_sentiment, req.user_id, req.interview_id)

    logger.info(f"Sentiment analysis for interview={req.interview_id} job ID={job.id} enqueued!")

    return job.id # returns job id for polling later

def start_star_feedback_analysis(text: str) -> str:
    """
    Start the STAR feedback analysis job by adding it to the queue.
    
    Args:
        text (str): The text to analyze using the STAR method.
    Returns:
        str: The job ID of the queue STAR feedback analysis job.
    """
    data = {"text": text} # predict_star_scores expects a dict with "text" key
    # Enqueue STAR feedback analysis job
    job = add_task_to_queue("high", predict_star_scores, data)

    return job.id

def start_feedback_analysis(req: AnalyzeInterviewRequest) -> str:
    """
    Start the full interview feedback analysis job (STAR + competency) by adding it to the queue.

    Args:
        req (AnalyzeInterviewRequest): Request containing user_id and interview_id.
    Returns:
        str: The Redis job ID of the queued feedback analysis job.
    """
    logger.info(f"Starting feedback analysis job for interview={req.interview_id}.")

    job = add_task_to_queue("high", analyze_interview_feedback, req.user_id, req.interview_id)

    logger.info(
        f"Feedback analysis for interview={req.interview_id} job ID={job.id} enqueued!"
    )

    return job.id


def start_interview_analysis(req: AnalyzeInterviewRequest) -> str:
    """
    Start the interview analysis job by adding it to the task queue.
    
    Enqueues both audio sentiment analysis and full feedback analysis (STAR + competency)
    to run concurrently as separate background jobs.

    Args:
        req (AnalyzeInterviewRequest): Request body that contains the fields needed to perform the various interview analysis tasks.
    Returns:
        str: The job ID of the queued feedback analysis job.
    """
    # Enqueue audio sentiment analysis job
    sentiment_analysis_request = SentimentAnalysisRequest(user_id=req.user_id, interview_id=req.interview_id)
    start_audio_analysis(sentiment_analysis_request)

    # Enqueue full feedback analysis job (STAR + competency); returns this job id for polling
    feedback_job_id = start_feedback_analysis(req)

    return feedback_job_id