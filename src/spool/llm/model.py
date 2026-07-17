import sys
from src.exception import MyException
from src.logger import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.infra.config import PARAMS_CONFIGS

load_dotenv()


class ChatModel:
    """Initializes and configures the active Google Gemini language model."""

    def __init__(self) -> None:
        """
        Initialize the language model configuration.

        Raises:
            MyException: If configuring the language model fails.
        """
        try:
            self.model_name = PARAMS_CONFIGS["LLM"]["model"]
            self.temperature = PARAMS_CONFIGS["LLM"]["temperature"]
            logging.info(f"Init ChatModel: {self.model_name}")
            self.model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
                model=self.model_name,
                temperature=self.temperature,
            )
            logging.info("ChatModel ready.")

        except Exception as e:
            logging.error(
                f"Error configuring ChatModel engine API references natively: {e}"
            )
            raise MyException(e, sys) from e
