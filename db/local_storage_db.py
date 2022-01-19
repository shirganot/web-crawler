from uuid import uuid4
import os
import json
from .db import DB
from typing import Dict, Sequence, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)


class LocalStorageDB(DB):
    _LOCAL_FILES_DB_ROOT_DIRECTORY = "store"

    def __init__(self, directory):
        self.original_directory = directory
        self.directory = os.path.join(
            LocalStorageDB._LOCAL_FILES_DB_ROOT_DIRECTORY, directory
        )

    def __handle_directory(self) -> None:
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def insert(self, data: Dict, id: str = uuid4()) -> bool:
        try:
            self.__handle_directory()
            file_route = os.path.join(self.directory, f"{id}.json")
            with open(file_route, "x") as f:
                f.write(json.dumps(data))
            return True
        except FileNotFoundError:
            logger.warning(
                "FileNotFoundError. It could be a problem with the directory"
                f" name - {self.directory}"
            )
            self.__handle_directory()
            return False
        except FileExistsError as err:
            logger.error(
                "Looks like the program is trying to insert an exist data -"
                f"{err}"
            )
            return False
        except Exception as err:
            logger.error(
                "Something went wrong while inserting data to LocalFileDB -"
                f" {err}"
            )
            return False

    def insert_many(self, data_sequence: Sequence[Dict[str, Any]]) -> bool:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.insert, data, data.get("id", uuid4()))
                for data in data_sequence
            ]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as err:
                    logger.error(
                        "Sometihng went wrong while creating files in"
                        f" threads - {err}"
                    )
                    return False
                finally:
                    return True
