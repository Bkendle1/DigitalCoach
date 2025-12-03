"""
User's Performance Feedback Schemas
"""

from pydantic import BaseModel, Field, field_validator, confloat
from typing import List, Optional
from schemas.jobs import JobStatus

class BigFiveScoreResult(BaseModel):
    """
    Big Five Score Analysis
    """

    o: float  # Openness
    c: float  # Conscientiousness
    e: float  # Extraversion
    a: float  # Agreeableness
    n: float  # Neuroticism
    _disclaimer: Optional[str] = None # Optional Disclaimer about score interpretation

class CompetencyFeedback(BaseModel):
    """
    Feedback for a specific competency
    """

    score: float # Overall score
    strengths: List[str] = Field(default_factory=list)  # List of strengths displayed in interview
    areas_for_improvement: List[str] = Field(default_factory=list) # List of areas to improve
    recommendations: List[str] = Field(default_factory=list) # Recommended course of action

class OverallCompetencyFeedback(BaseModel):
    """
    Overall Competency Feedback
    """

    communication_clarity: CompetencyFeedback # Feedback on communication clarity
    confidence: CompetencyFeedback # Feedback on confidence
    engagement: CompetencyFeedback # Feedback on engagement
    overall_score: float # Overall score
    summary: str   # Summary of overall performance
    key_recommendations: List[str] = Field(default_factory=list) # Specific actions to take

class StructureDetails(BaseModel):
    """
    Metrics for text structure analysis
    """

    paragraph_count: int = 0
    avg_paragraph_length: int = 0
    transition_words: int = 0
    has_intro: bool = False
    has_conclusion: bool = False
    sentence_variety: int = 0

class TextStructureResult(BaseModel):
    """
    Text Structure Analysis
    """

    prediction_score: float
    binary_prediction: int
    output_text: str
    details: StructureDetails = Field(default_factory=StructureDetails)

class StarFeedbackRequest(BaseModel):
    """
    Request model for STAR feedback
    """
    
    text: str
    @field_validator("text")
    def validate_text(cls, value):
        if not value or len(value.strip()) < 10:
            raise ValueError("Text is too short for analysis. Please provide a more detailed response.")
        return value


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