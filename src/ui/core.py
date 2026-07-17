import json
import urllib.request
import sys

import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import Runnable

from src.spool.llm.model import ChatModel
from src.spool.data.store import ChromaStore
from src.spool.data.splitter import TranscriptSplitter
from src.spool.data.loader import YouTubeTranscriptLoader
from src.spool.llm.prompt_generator import PromptGenerator
from src.spool.llm.retriever import Retriever as BM25Wrapper
from langchain.retrievers import EnsembleRetriever  # type: ignore
from typing import Any
from src.exception import MyException
from src.logger import logging


def initialize_session_state() -> None:
    """Initialize necessary Streamlit session state variables."""
    logging.info("Init session state...")
    if "video_id" not in st.session_state:
        st.session_state.video_id = "9M_QK4stCJU"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state.messages = []


@st.cache_resource
def initialize_pipeline(video_id: str) -> tuple[Any, Runnable]:
    """
    Construct the Langchain pipeline for querying a YouTube transcript.

    Args:
        video_id (str): The video ID to analyze.

    Returns:
        tuple[Any, Runnable]:
            - The configured Retriever instance and the Langchain query pipeline.
    """
    try:
        logging.info("Configuring pipeline...")
        loader = YouTubeTranscriptLoader()
        transcript = loader.fetch(video_id=video_id)

        splitter = TranscriptSplitter()
        chunks = splitter.split(transcript)

        chroma_store = ChromaStore(persist_directory=f"chroma/store_{video_id}")
        existing_docs = chroma_store.get_docs(include=["metadatas"])
        if not existing_docs.get("metadatas"):
            chroma_store.add_docs(docs=chunks)

        vector_retriever = chroma_store.retriever

        bm25_wrapper = BM25Wrapper(docs=chunks)
        bm25_retriever = bm25_wrapper.retriever

        retriever = EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever], weights=[0.5, 0.5]
        )
        model = ChatModel().model

        prompt = PromptGenerator().prompt
        parser = StrOutputParser()

        chain = prompt | model | parser
        logging.info("Pipeline ready.")
        return retriever, chain

    except Exception as e:
        logging.error(f"Critical error initializing pipeline dependencies: {e}")
        st.error(f"Critical error initializing pipeline dependencies: {e}")
        st.stop()
        raise


@st.cache_data
def get_video_title(video_id: str) -> str:
    """
    Fetch the video title from the official YouTube oEmbed API.

    Args:
        video_id (str): The video ID to look up.

    Returns:
        str:
            - The video title, or a placeholder if the request fails.
    """
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    try:
        logging.info(f"Fetching title: {video_id}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get("title", f"Video {video_id}")

    except Exception as e:
        logging.warning(f"Error quietly suppressing oEmbed title grab fail: {e}")
        return f"Video {video_id}"
