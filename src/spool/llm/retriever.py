import sys
from src.exception import MyException
from src.logger import logging
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from src.infra.config import PARAMS_CONFIGS


class Retriever:
    """Uses a BM25 sparse retriever to search document collections."""

    def __init__(self, docs: list[Document]) -> None:
        """
        Initialize the BM25 retriever with the loaded documents.

        Args:
            docs (list[Document]): A list of initialized Langchain Documents.

        Raises:
            MyException: If initializing the retriever fails.
        """
        try:
            logging.info("Init BM25Retriever...")
            self.retriever = BM25Retriever.from_documents(docs)
            self.retriever.k = PARAMS_CONFIGS["RETRIEVER"]["k"]
            logging.info("Retriever ready.")

        except Exception as e:
            logging.error(f"Error initializing BM25 retriever: {e}")
            raise MyException(e, sys) from e
