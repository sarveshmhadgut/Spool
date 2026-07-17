import re
import sys
from typing import Iterable
from src.exception import MyException
from src.logger import logging
from dotenv import load_dotenv
from youtube_transcript_api import (
    FetchedTranscriptSnippet,
    YouTubeTranscriptApi,
    TranscriptsDisabled,
)


class YouTubeTranscriptLoader:
    """Fetches and cleans transcripts from YouTube videos."""

    def __init__(self) -> None:
        """Initialize the loader and the YouTube Transcript API."""

        load_dotenv()
        self.api: YouTubeTranscriptApi = YouTubeTranscriptApi()

    def _clean_text(self, text: str) -> str:
        """
        Clean transcript text by removing newlines and bracketed metadata.

        Args:
            text (str): The raw transcript text chunk.

        Returns:
            str:
                - The cleaned text.
        """
        text = text.replace("\n", " ")
        text = re.sub(r"\[.*?\]", "", text)

        return text.strip()

    def fetch(self, video_id: str) -> str:
        """
        Fetch the complete English transcript for a given YouTube video.

        Args:
            video_id (str): The YouTube video ID.

        Returns:
            str:
                - The concatenated transcript text, or an empty string if unavailable.

        Raises:
            MyException: If fetching the transcript fails.
        """
        try:
            logging.info("Loading transcript list...")
            transcripts: Iterable[FetchedTranscriptSnippet] = self.api.fetch(
                video_id=video_id, languages=["en"]
            )
            logging.info("Transcript list loaded.")

            text: str = " ".join(
                [
                    self._clean_text(transcript.text)
                    for transcript in transcripts
                    if "♪" not in transcript.text
                    and len(self._clean_text(transcript.text)) > 0
                ]
            )

            cleaned_text = text.strip()
            logging.info("Transcript fetched.")
            return cleaned_text

        except TranscriptsDisabled:
            logging.warning("Transcripts disabled.")
            return ""

        except Exception as e:
            logging.error(f"Error retrieving transcript: {e}")
            raise MyException(e, sys) from e
