import pytest
from unittest.mock import patch, MagicMock

from mlapi.tasks.assemblyai_api_transcript import transcribe_audio


def test_transcribe_audio_success():
    fake_transcript = MagicMock()
    fake_transcript.error = None
    fake_transcript.text = "Hello world"

    fake_transcriber = MagicMock()
    fake_transcriber.transcribe.return_value = fake_transcript

    with patch("mlapi.tasks.assemblyai_api_transcript.aai.Transcriber", return_value=fake_transcriber):
        with patch("mlapi.tasks.assemblyai_api_transcript.aai.settings"):
            text = transcribe_audio("sample.wav")

    assert text == "Hello world"


def test_transcribe_audio_raises_on_error():
    fake_transcript = MagicMock()
    fake_transcript.error = "Something went wrong"
    fake_transcript.text = None

    fake_transcriber = MagicMock()
    fake_transcriber.transcribe.return_value = fake_transcript

    with patch("mlapi.tasks.assemblyai_api_transcript.aai.Transcriber", return_value=fake_transcriber):
        with patch("mlapi.tasks.assemblyai_api_transcript.aai.settings"):
            with pytest.raises(Exception):
                transcribe_audio("sample.wav")


def test_transcribe_audio_returns_empty_string_if_no_text():
    fake_transcript = MagicMock()
    fake_transcript.error = None
    fake_transcript.text = ""

    fake_transcriber = MagicMock()
    fake_transcriber.transcribe.return_value = fake_transcript

    with patch("mlapi.tasks.assemblyai_api_transcript.aai.Transcriber", return_value=fake_transcriber):
        with patch("mlapi.tasks.assemblyai_api_transcript.aai.settings"):
            text = transcribe_audio("sample.wav")

    assert text == ""
