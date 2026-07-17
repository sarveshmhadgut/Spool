import sys
from dotenv import load_dotenv
from typing import List, Dict, Any
from src.exception import MyException
from src.logger import logging
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from src.infra.config import PARAMS_CONFIGS

load_dotenv()


class ChromaStore:
    """Manages the local ChromaDB vector store for transcript embeddings."""

    def __init__(self, persist_directory: str = "chroma_vector_store") -> None:
        """
        Initialize the ChromaDB vector store and Google embeddings.

        Args:
            persist_directory (str): The local directory to save the ChromaDB database.

        Raises:
            MyException: If initializing the ChromaDB store fails.
        """
        try:
            logging.info("Init ChromaStore...")
            self.persist_directory: str = persist_directory
            self.embeddings: GoogleGenerativeAIEmbeddings = (
                GoogleGenerativeAIEmbeddings(
                    model=PARAMS_CONFIGS["EMBEDDINGS"]["model"]
                )
            )
            self.store: Chroma = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
            )
            logging.info("ChromaStore ready.")
            self.retriever: VectorStoreRetriever = self.store.as_retriever(
                search_type=PARAMS_CONFIGS["STORE_RETRIEVER"]["search_type"],
                search_kwargs=PARAMS_CONFIGS["STORE_RETRIEVER"]["search_kwargs"],
            )
        except Exception as e:
            logging.error(f"Failed to initialize ChromaStore: {e}")
            raise MyException(e, sys) from e

    def add_docs(self, docs: list[Document]) -> None:
        """
        Add document chunks to the ChromaDB vector store.

        Args:
            docs (list[Document]): The list of Langchain Documents to insert.

        Raises:
            MyException: If persisting documents fails.
        """
        try:
            if not docs:
                return
            logging.info(f"Saving {len(docs)} docs...")
            self.store.add_documents(documents=docs)
            logging.info("Docs saved.")

        except Exception as e:
            logging.error(f"Error persisting documents to vector store: {e}")
            raise MyException(e, sys) from e

    def get_docs(self, include: List[str] | None = None) -> Dict[str, Any]:
        """
        Fetch documents and metadata from the ChromaDB store.

        Args:
            include (List[str] | None): Attributes to return. Defaults to ["documents", "metadatas"].

        Returns:
            Dict[str, Any]:
                - The requested database items.

        Raises:
            MyException: If fetching documents fails.
        """
        try:
            logging.info("Fetching docs...")
            if include is None:
                include = ["documents", "metadatas"]
            res = self.store.get(include=include)
            logging.info("Docs fetched.")
            return res

        except Exception as e:
            logging.error(f"Failed to extract document map from Vector database: {e}")
            raise MyException(e, sys) from e
