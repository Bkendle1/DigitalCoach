# User's Performance Feedback Schemas
from pydantic import BaseModel, Field
from typing import List

class BigFiveScoreResult(BaseModel):
    """
    Big Five Score Analysis
    """

    o: float
    c: float
    e: float
    a: float
    n: float
    _disclaimer: str

class CompetencyFeedback(BaseModel):
    """
    Competency Feedback
    """

    score: float
    strengths: List[str] = Field(default_factory=list)
    areas_for_improvement: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)

class OverallCompetencyFeedback(BaseModel):
    """
    Overall Competency Feedback
    """

    communication_clarity: CompetencyFeedback
    confidence: CompetencyFeedback
    engagement: CompetencyFeedback
    overall_score: float
    summary: str
    key_recommendations: List[str] = Field(default_factory=list)

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

