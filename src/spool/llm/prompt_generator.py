import sys
from src.exception import MyException
from src.logger import logging
from langchain_core.prompts import ChatPromptTemplate
from src.infra.config import PROMPTS_CONFIGS


class PromptGenerator:
    """Constructs prompt templates for formatting Chat LLM inputs."""

    def __init__(self) -> None:
        """
        Initialize the system prompt constraints and templates.

        Raises:
            MyException: If generating the prompt template fails.
        """
        try:
            logging.info("Init prompt generator...")
            self.system_prompt = PROMPTS_CONFIGS["SYSTEM_PROMPT"]

            self.prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
                [
                    ("system", self.system_prompt),
                    ("human", "{user_message}"),
                ]
            )
            logging.info("Prompt generator ready.")

        except Exception as e:
            logging.error(f"Error generating prompt template bindings: {e}")
            raise MyException(e, sys) from e
