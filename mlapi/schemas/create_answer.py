# Builds the final response schema
from typing import List, Optional
from pydantic import BaseModel, Field
from schemas.feedback import BigFiveScoreResult, OverallCompetencyFeedback
from schemas.audio import HighlightData
from schemas.jobs import JobStatus

class TimelineStructure(BaseModel):
    """
    Timeline Structure Analysis
    """

    start: int  # in milliseconds
    end: int  # in milliseconds
    audioSentiment: str

class CreateAnswerEvaluation(BaseModel):
    """
    Result of creating an answer
    """

    timeline: List[TimelineStructure] = Field(default_factory=list)
    isStructured: int  # 1 or 0
    predictionScore: float  # 0-100
    overallSentiment: str  # Overall audio sentiment from assemblyAI
    topFiveKeywords: List[HighlightData] = Field(default_factory=list)
    transcript: str  # Full transcript of speech
    bigFive: BigFiveScoreResult
    competencyFeedback: OverallCompetencyFeedback
    aggregateScore: float = 0.0  # Overall score (0-100)


class CreateAnswer(BaseModel):
    """
    Result of creating an answer
    """

    evaluation: CreateAnswerEvaluation

class CreateAnswerJobResponse(BaseModel):
    """
    Response model for polling answer job status
    """
    job_id: str
    status: JobStatus
    result: Optional[CreateAnswer] = None
    error: Optional[str] = None