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
    LLM-identified breakdown of each STAR component in the candidate's response
    """

    situation: str  # Situation described by the candidate
    task: str       # Task or goal described by the candidate
    action: str     # Actions the candidate took
    result: str     # Measurable results or outcomes


class LLMStarPercentages(BaseModel):
    """
    LLM-estimated percentage of response dedicated to each STAR component
    """

    situation_percentage: int
    task_percentage: int
    action_percentage: int
    result_percentage: int


class LLMStarFeedback(BaseModel):
    """
    LLM response for STAR method analysis
    """

    star_breakdown: StarBreakdown           # Identified STAR components
    star_percentages: LLMStarPercentages    # Estimated percentage breakdown
    overall_score: float                    # Score rating STAR adherence (0-10)
    feedback: str                           # Actionable feedback to improve STAR usage


class InterviewFeedbackResponse(BaseModel):
    """
    Response model for an interview feedback analysis job
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