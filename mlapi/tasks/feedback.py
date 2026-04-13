"""
Task functions for interview feedback analysis

Saves results to Firestore
"""

import os
from openai import OpenAI
from pydantic import ValidationError
from dotenv import load_dotenv

from data.interviews import getTranscriptById
from services.firebase_setup import get_firestore_client
from schemas.feedback import LLMStarFeedback, OverallCompetencyFeedback
from schemas.interview import Feedback, OverallCompetency, CompetencyMetric
from tasks.prompts import STAR_PROMPT, COMPETENCY_FEEDBACK_PROMT
from utils.logger_config import get_logger

load_dotenv()
logger = get_logger(__name__)

async def analyze_star_feedback(user_id: str, interview_id: str) -> LLMStarFeedback:
    """
    Analyzes an interview transcript using the STAR method via LLM.
    Fetches the interview transcript from Firestore, sends it to the LLM with
    the STAR_PROMPT, and returns validated STAR feedback.
    Args:
        user_id (str): ID of the user that owns the interview.
        interview_id (str): ID of the interview to analyze.
    Returns:
        LLMStarFeedback: Validated STAR feedback including breakdown, percentages, score, and feedback text.
    Raises:
        Exception: If the LLM call fails or the response cannot be validated.
    """
    logger.info(f"Starting STAR feedback analysis for interview={interview_id}...")

    base_url = os.getenv("LM_BASE_URL")
    api_key = os.getenv("LM_API_KEY")
    model_name = os.getenv("MODEL")

    client = OpenAI(base_url=base_url, api_key=api_key)

    transcript = await getTranscriptById(user_id, interview_id)

    model_messages = [
        {"role": "system", "content": STAR_PROMPT},
        {"role": "user", "content": transcript},
    ]

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=model_messages,
        )
    except Exception as e:
        logger.error(f"Error communicating with LLM for STAR analysis on interview={interview_id}: {e}")
        raise

    try:
        llm_response = response.choices[0].message.content
        logger.info(f"LLM STAR response for interview={interview_id}: {llm_response}")
        validated_data = LLMStarFeedback.model_validate_json(llm_response)
        logger.info(f"STAR feedback analysis for interview={interview_id} successful!")
        return validated_data
    except ValidationError as e:
        logger.error(
            f"LLM STAR response for interview={interview_id} has invalid shape. "
            f"Response: {llm_response} Reason: {e}"
        )
        raise

async def analyze_competency_feedback(user_id: str, interview_id: str) -> OverallCompetencyFeedback:
        """
    Analyzes an interview transcript for competency feedback via LLM.
    Evaluates the candidate's confidence, communication clarity, and engagement
    by sending the transcript to the LLM with the COMPETENCY_FEEDBACK_PROMT.

    Args:
        user_id (str): ID of the user that owns the interview.
        interview_id (str): ID of the interview to analyze.
    Returns:
        OverallCompetencyFeedback: Validated competency feedback including per-competency scores and a summary.
    Raises:
        Exception: If the LLM call fails or the response cannot be validated.
    """
        logger.info(f"Starting competency feedback analysis for interview={interview_id}...")

        base_url = os.getenv("LM_BASE_URL")
        api_key = os.getenv("LM_API_KEY")
        model_name = os.getenv("MODEL")

        client = OpenAI(base_url=base_url, api_key=api_key)

        transcript = await getTranscriptById(user_id, interview_id)

        model_messages = [
             {"role": "system", "content": COMPETENCY_FEEDBACK_PROMT},
             {"role": "user", "content:": transcript},
        ]

        try:
             response = client.chat.completions.create(
                  model_name,
                  messages=model_messages,
             )
        except Exception as e:
             logger.error(
                  f"Error communicating with LLM for competency analysis on interview={interview_id}: {e}"
             )
             raise
        
        try:
             llm_response = response.choices[0].message.content
             logger.info(f"LLM competency response for interview={interview_id}: {llm_response}")
             validated_data = OverallCompetencyFeedback.model_validate_json(llm_response)
             logger.info(f"Competency feedback analysis for interview={interview_id} successful!")
             return validated_data
        except ValidationError as e:
             logger.error(
                  f"LLM competency response for interview={interview_id} has invalid shape. "
                  f"Response: {llm_response} Reason: {e}"
             )
             raise
        
async def analyze_interview_feedback(user_id: str, interview_id: str) -> Feedback:
    """
    Runs full interview feedback analysis (STAR + competency) and saves results to Firestore.
    Executes STAR and competency analyses sequentially, maps the LLM results to the
    Feedback schema stored in the interview document, and marks the interview as analyzed.
    Args:
        user_id (str): ID of the user that owns the interview.
        interview_id (str): ID of the interview to analyze.
    Returns:
        Feedback: The combined interview feedback saved to Firestore.
    Raises:
        Exception: If either analysis fails or the Firestore update fails.
    """
    logger.info(f"Starting full interview feedback analysis for interview={interview_id}...")

    star_result = await analyze_star_feedback(user_id, interview_id)
    competency_result = await analyze_competency_feedback(user_id, interview_id)

    overall_competency = OverallCompetency(
         clarity=CompetencyMetric(
              score=int(round(competency_result.communication_clarity.score)),
              summary=competency_result.communication_clarity.evaluation,
         ),
                 confidence=CompetencyMetric(
            score=int(round(competency_result.confidence.score)),
            summary=competency_result.confidence.evaluation,
        ),
        engagement=CompetencyMetric(
            score=int(round(competency_result.engagement.score)),
            summary=competency_result.engagement.evaluation,
        ),
        star=CompetencyMetric(
            score=int(round(star_result.overall_score)),
            summary=star_result.feedback,
        ),
    )

    ai_feedback = (
         f"STAR Score: {star_result.overall_score}/10\n"
         f"{star_result.feedback}\n\n"
         f"Overall Competency Score: {competency_result.overall_score}/10\n"
        f"{competency_result.summary}"
    )

    feedback = Feedback(ai_feedback=ai_feedback, overall_competency=overall_competency)

    db = get_firestore_client()
    interview_ref = (
         db.collection("users")
         .document(user_id)
         .collection("interviews")
         .document(interview_id)
    )
    await interview_ref.update({
         "feedback": feedback.model_dump(),
         "is_analyzed": True,
    })

    logger.info(
         f"Full interview feedback for interview={interview_id} saved to Firestore successfully!"
    )

    return feedback


