# Handles orchestration of tasks for interview videos, e.g. starting analysis jobs. 
# Can be called by route handlers.

from tasks.assemblyai_api import detect_audio_sentiment
from redisStore.queue import add_task_to_queue
from tasks.create_answer_task import create_answer

def start_interview_analysis(video_url: str) -> str:
    """
    Start the interview analysis job by adding it to the task queue.
    
    Currently, this function only starts the audio sentiment job but can be extended to also start facial analysis.

    Args:
        video_url (str): The URL of the video to analyze.
    Returns:
        str: The job ID of the queued interview analysis job.
    """
    # Enqueue audio analysis job on the given video url
    audio_job = add_task_to_queue(detect_audio_sentiment, video_url)

    # Start the create_answer job that's dependent on the analysis job(s) 
    job = add_task_to_queue(create_answer, video_url, audio_job.get_id())

    return job.get_id()

