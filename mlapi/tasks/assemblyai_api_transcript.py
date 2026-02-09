import os
import assemblyai as aai
from mlapi.utils.logger_config import get_logger

ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")
logger = get_logger(__name__)


def transcribe_audio(audio_url: str) -> str:
    """
    Sends an audio or video file to AssemblyAI and returns the transcript

    """
    if not ASSEMBLY_API_KEY:
        raise RuntimeError("AssemblyAI API key not found in environment (ASSEMBLY_API_KEY)")

    aai.settings.api_key = ASSEMBLY_API_KEY
    transcriber = aai.Transcriber()

    logger.info(f"Transcribing audio: {audio_url}")
    transcript = transcriber.transcribe(audio_url)

    if transcript.error:
        logger.error(f"AssemblyAI transcription error: {transcript.error}")
        raise RuntimeError(transcript.error)

    logger.info("Transcription completed successfully")
    return transcript.text


# Local testing

if __name__ == "__main__":
    test_audio = "sample.wav" 
    text = transcribe_audio(test_audio)
    print("\nTRANSCRIPT:\n")
    print(text)
