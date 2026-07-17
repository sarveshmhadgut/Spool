import sys
from pathlib import Path
from typing import Any, Dict
import yaml  # type: ignore
from src.exception import MyException

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

try:
    PARAMS_CONFIGS: Dict[str, Any] = yaml.safe_load(
        (ROOT_DIR / "configs/params.yaml").read_text()
    )
    PROMPTS_CONFIGS: Dict[str, Any] = yaml.safe_load(
        (ROOT_DIR / "configs/prompts.yaml").read_text()
    )
except Exception as e:
    raise MyException(e, sys) from e
