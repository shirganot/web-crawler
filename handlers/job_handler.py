import schedule
import time
from typing import Callable
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class IntervalUnits(Enum):
    MINUTES = "minutes"
    SECONDS = "seconds"
    HOURS = "hours"


class JobHandler:
    def __init__(
        self, interval_amount: int = 0, interval_units: str = "minutes"
    ):
        assert interval_amount > 0, "'interval_amount' should be bigger then 0"

        self.interval_amount = interval_amount
        self.interval_units = interval_units
        self.__is_job_initialized = False

    def schedule_a_job(self, fn: Callable) -> None:
        try:
            if self.__is_job_initialized:
                return

            match self.interval_units:
                case IntervalUnits.MINUTES.value:
                    self.__schedule_a_job_by_minutes(fn)
                case IntervalUnits.SECONDS.value:
                    self.__schedule_a_job_by_seconds(fn)
                case IntervalUnits.HOURS.value:
                    self.__schedule_a_job_by_hours(fn)
                case _:
                    raise Exception(
                        f"We don't support {self.interval_units} interval"
                        " units"
                    )

            self.__is_job_initialized = True

            while True:
                schedule.run_pending()
                time.sleep(1)
        except Exception as err:
            logger.error(f"Something went wrong while creating a job - {err}")

    def __schedule_a_job_by_minutes(self, fn: Callable) -> None:
        schedule.every(self.interval_amount).minutes.do(fn)

    def __schedule_a_job_by_seconds(self, fn: Callable) -> None:
        schedule.every(self.interval_amount).seconds.do(fn)

    def __schedule_a_job_by_hours(self, fn: Callable) -> None:
        schedule.every(self.interval_amount).hours.do(fn)
