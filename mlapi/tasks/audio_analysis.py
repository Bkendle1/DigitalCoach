from schemas import (
    SentimentAnalysisResult,
    StarFeedbackEvaluation
)
from utils.logger_config import get_logger
import os
from openai import OpenAI
from pydantic import ValidationError
from dotenv import load_dotenv
from data.interviews import getTranscriptById
from services.firebase_init import get_firestore_client
from tasks.prompts import (
    SENTIMENT_ANALYSIS_PROMPT,
    STAR_PROMPT
) 
logger = get_logger(__name__)

load_dotenv() # load environment variables
async def detect_audio_sentiment(user_id: str, interview_id: str) -> SentimentAnalysisResult:
    """
    Generate audio sentiment analysis using local LLM. This should be a job performed by a Redis RQ Worker.

    Args:
        user_id (str): User id that owns the interview to be analyzed.
        interview_id (str): Id of the interview undergoing sentiment analysis
    Returns:
        result (SentimentAnalysisResult): Sentiment analysis results according to SentimentAnalysisResult schema
    """

    logger.info(f"Starting sentiment analysis on interview={interview_id}...")

    # extract relevant environment variables
    base_url = os.getenv("LM_BASE_URL")
    api_key = os.getenv("LM_API_KEY")
    model_name = os.getenv("MODEL")
    # initialize OpenAI-compliant LLM client
    client = OpenAI(base_url=base_url, api_key=api_key)

    # get interview's transcript
    transcript = await getTranscriptById(user_id, interview_id)

    # initialize messages for LLM 
    # system messages provide additional context to the LLM
    # user messages are the messages the LLM actually responds to
    model_messages = [
                {
                    "role": "system",
                    "content": SENTIMENT_ANALYSIS_PROMPT
                },
                {
                    "role": "user",
                    "content": transcript # pass the transcript to the LLM for sentiment analysis
                }
            ]
    try:
        response = client.chat.completions.create(
            model=model_name, # llm model name from docker model runner (you can find this by running `docker model list` in your CMD)
            messages = model_messages,
        )

    except Exception as e:
        logger.error(f"Error communicating with LLM: {e}")
        logger.error(f"Sentiment analysis for interview={interview_id} failed. Will attempt a retry...")
        # return SentimentAnalysisResult(error=f"Error communicating with LLM: {e}")
        raise BaseException(e) # to make sure the RQ job returns a failed status, we must raise an exception
    
    db = get_firestore_client()
    # parse and return LLM response
    try:
        logger.info(f"Verifying LLM sentiment analysis on interview={interview_id}...")

        llm_response = response.choices[0].message.content # extract LLM's JSON response string
        logger.info(f"LLM response={llm_response}")
        # verify LLM JSON response is the correct shape 
        validated_data = SentimentAnalysisResult.model_validate_json(llm_response) # parses JSON string, checks if it fits our response schema and instantiates our schema if successful 
        logger.info(f"Sentiment Analysis on interview={interview_id} successful!")

        # add sentiment analysis to user's interview as a JSON string to be parsed later and converted into an overall sentiment
        # get reference to interview
        interviewRef = db.collection("users").document(user_id).collection("interviews").document(interview_id)
        await interviewRef.update({"sentiment": validated_data.model_dump_json()})

        return validated_data
    except ValidationError as e:
        logger.error(f"LLM sentiment analysis on interview={interview_id} is in invalid shape. Reason: {e} Will attempt to retry...")
        # return SentimentAnalysisResult(error=f"LLM sentiment analysis on interview={interview_id} is in invalid shape. Reason: {e}")
        raise ValidationError(f"LLM sentiment analysis on interview={interview_id} is in invalid shape: {llm_response} Reason: {e}") # to make sure the RQ job returns a failed status, we must raise an exception

async def star_analysis(user_id: str, interview_id: str):
    """
    Perform STAR analysis using local LLM. This should be a job performed by a Redis RQ Worker.

    Args:
        user_id (str): User id that owns the interview to be analyzed.
        interview_id (str): Interview id of the interview undergoing STAR analysis.

    Returns:
        result (StarFeedbackEvaluation): STAR analysis results according to StarFeedbackEvaluation schemas 
    """

    logger.info(f"Starting STAR analysis on interview={interview_id}...")

    # extract relevant environment variables
    base_url = os.getenv("LM_BASE_URL")
    api_key = os.getenv("LM_API_KEY")
    model_name = os.getenv("MODEL")

    # initialize OpenAI-compliant LLM client
    client = OpenAI(base_url=base_url, api_key=api_key)

    # get interview's transcript
    transcript = await getTranscriptById(user_id, interview_id)

    # initialize messsages for LLM
    # system messages provide additional context to the LLM before inference
    # user messages are messages that the LLM responds to
    model_messages = [
        {
            "role": "system",
            "content": STAR_PROMPT
        },
        {
            "role": "user",
            "content": transcript # pass the transcript to the LLM for star analysis
        }
    ]
    
    # send task to local LLM
    try:
        response = client.chat.completions.create(
            model=model_name, # llm model name from docker model runner (you can find this by running `docker model list` in your CMD)
            messages = model_messages,
        )
    except Exception as e:
        logger.error(f"Error communicating with LLM: {e}")
        logger.error(f"STAR analysis for interview={interview_id} failed. Will attempt a retry...")
        raise BaseException(e) # raise exception to set failed job status
    

    db = get_firestore_client()

    # parse and return LLM response
    try:
        logger.info(f"Verifying LLM STAR analysis on interview={interview_id}...")

        llm_response = response.choices[0].message.content
        # extract LLM's JSON response string
        logger.info(f"LLM response={llm_response}")
        # verify LLM JSON response is the correct shape
        validated_data = StarFeedbackEvaluation.model_validate_json(llm_response) # parse JSON string, if it matches the schema then instantiate; otherwise throw
        logger.info(f"STAR analysis on interview={interview_id} successful!")

        data = validated_data.model_dump() # generate dictionary of validated llm response
        
        # NOTE: Currently, we only store the final score and overall feedback from STAR analysis but feel free to use the entire LLM response. However, you may have to update the related schemas/interfaces from the backend and frontend to reflect the new shape.
        star_response = {
            "score": data["overall_score"],
            "summary": data["feedback"],
        }

        # add STAR analysis to user's interview
        # get reference to interview
        interviewRef = db.collection("users").document(user_id).collection("interviews").document(interview_id)
        await interviewRef.update({"feedback.overall_competency.star": star_response})

        return star_response
    except ValidationError as e:
        logger.error(f"LLM STAR analysis on interview={interview_id} is in invalid shape. Reason: {e} Will attempt to retry...")
        raise ValidationError(f"LLM STAR analysis on interview={interview_id} is in invalid shape. Reason: {e} Will attempt to retry...") # raise error to set RQ job to failed status