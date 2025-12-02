from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any, List
from enum import Enum
from schemas import AudioSentimentResult


class JobStatus(str, Enum):
    """
    Status of a job
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobId(BaseModel):
    """
    Job ID response model
    """

    job_id: str


class JobResponse(BaseModel):
    """
    Generic job response with status
    """

    job_id: str
    status: JobStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class CreateAnswerJobRequest(BaseModel):
    """
    Request to create an answer job
    """
    video_url: HttpUrl # URL of the video to analyze


class JobsListResponse(BaseModel):
    """
    Response model for listing jobs
    """

    jobs: List[JobResponse] = Field(default_factory=list)

class AudioAnalysisJob(BaseModel):
    """
    AssemblyAI API job details
    """

    video_url: str
    job_id: str
    status: JobStatus = JobStatus.PENDING
    result: Optional[AudioSentimentResult] = None