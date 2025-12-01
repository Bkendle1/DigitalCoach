# Builds the final response schema
from typing import List
from pydantic import BaseModel, Field
from schemas.audio import HighlightData
from schemas.feedback import BigFiveScoreResult, OverallCompetencyFeedback

class TimelineStructure(BaseModel):
    """
    Timeline Structure Analysis
    """

    start: int  # in milliseconds
    end: int  # in milliseconds
    audioSentiment: str
    # facialEmotion: List[str] = Field(default_factory=list)

class CreateAnswerEvaluation(BaseModel):
    """
    Result of creating an answer
    """

    timeline: List[TimelineStructure] = Field(default_factory=list)
    isStructured: int  # 1 or 0
    predictionScore: float  # 0-100
    # facialStatistics: FacialStatistics
    # overallFacialEmotion: str  # Most common facial emotion
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