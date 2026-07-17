import sys
from typing import List
from src.exception import MyException
from src.logger import logging
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.infra.config import PARAMS_CONFIGS


class TranscriptSplitter:
    """Splits large transcript strings into smaller Langchain Documents."""

    def __init__(self) -> None:
        """
        Initialize the text splitter.
        """
        logging.info("Init splitter...")
        self.chunk_size: int = PARAMS_CONFIGS["SPLITTER"]["chunk_size"]
        self.chunk_overlap: int = PARAMS_CONFIGS["SPLITTER"]["chunk_overlap"]
        self.splitter: RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        logging.info("Splitter ready.")

    def split(self, text: str) -> List[Document]:
        """
        Split the transcript text into Langchain Document chunks.

        Args:
            text (str): The full transcript text.

        Returns:
            List[Document]:
                - The split document chunks.

        Raises:
            MyException: If splitting the text fails.
        """
        try:
            if not text:
                return []

            logging.info("Splitting text...")
            docs: List[Document] = self.splitter.create_documents([text])
            logging.info(f"Created {len(docs)} chunks.")
            return docs

        except Exception as e:
            logging.error(f"Error during transcript splitting sequence: {e}")
            raise MyException(e, sys) from e
