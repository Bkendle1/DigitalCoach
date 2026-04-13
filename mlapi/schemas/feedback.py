"""
User's Performance Feedback Schemas
"""

from pydantic import BaseModel, Field
from typing import List
from schemas.jobs import JobStatus

class CompetencyFeedback(BaseModel):
    """
    Feedback for a specific competency
    """

    score: float # Overall score
    evaluation: str # States whether or not the user was compotent in some field 

class OverallCompetencyFeedback(BaseModel):
    """
    Overall Competency Feedback
    """

    communication_clarity: CompetencyFeedback  # Evaluation on communication clarity
    confidence: CompetencyFeedback # Evaluation on confidence
    engagement: CompetencyFeedback # Evaluation on engagement
    overall_score: float # Overall score
    summary: str # Summary of overall performance including evaluations for individual competencies

class StarBreakdown(BaseModel):
    """
    Breakdown of each STAR component
    """

    situation: str
    task: str
    action: str
    result:str

class LLMStarPercentages(BaseModel):
    """
    Percentage of response dedicated to each STAR component
    """

    situation_percentage: int
    task_percentage: int
    action_percentage: int
    result_percentage: int

class LLMStarFeedback(BaseModel):
    """
    LLM response for STAR method analysis
    """

    star_breakdown: StarBreakdown
    star_percentages: LLMStarPercentages
    overall_score: float
    feedback: str

class InterviewFeedbackResponse(BaseModel):
    """
    Response model for interview feedback analysis job
    """

    job_id: str
    status: JobStatus
    result: dict | None = None
    error: str | None = None

class StarFeedbackRequest(BaseModel):
    """
    Request model for STAR feedback
    """
    
    text: str

class StarClassification(BaseModel):
    """
    Classification result for a single sentence
    """

    sentence: str
    category: str


class StarPercentages(BaseModel):
    """
    Percentage breakdown of STAR components
    """

    action: float
    result: float
    situation: float
    task: float


class StarFeedbackEvaluation(BaseModel):
    """
    Results after performing STAR feedback analysis
    """

    fulfilled_star: bool
    percentages: StarPercentages
    classifications: List[StarClassification]
    feedback: List[str]

class StarFeedbackResponse(BaseModel):
    """
    Response model for STAR feedback job
    """

    job_id: str
    status: JobStatus
    result: StarFeedbackEvaluation | None = None
    error: str | None = None