from enum import Enum


class GetApiExecutionsStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
