from __future__ import annotations

from data.interviews import getTranscriptById
from services.firebase_setup import get_firestore_client
from utils.logger_config import get_logger
from tasks.helpers.filler_hedge_counter import count_filler_and_hedge

logger = get_logger(__name__)

async def analyze_filler_hedge(user_id: str, interview_id: str) -> dict:

    logger.info(f"Starting filler/hedge analysis for interview={interview_id}...")

    transcript = await getTranscriptById(user_id, interview_id)

    result = count_filler_and_hedge(transcript)

    db = get_firestore_client()
    interviewRef = (
        db.collection("users")
        .document(user_id)
        .collection("interviews")
        .document(interview_id)
    )

    await interviewRef.update({"metrics.filler_hedge": result})

    logger.info(f"Filler/hedge analysis stored for interview={interview_id}.")
    return result