from enum import Enum


class HttpTaskUpdateRequestStatus(str, Enum):
    FAILED = "failed"
    RUNNING = "running"
    SUCCESS = "success"

    def __str__(self) -> str:
        return str(self.value)
