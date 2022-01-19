import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def get_json_file(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(f"{path}.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        logger.error(f"There is no file exist in this path - {path}")
    except Exception as err:
        logger.error(
            f"Something went wrong while trying to reload a JSON file - {err}"
        )
