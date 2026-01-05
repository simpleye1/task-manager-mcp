from enum import Enum


class GetApiTasksIdentifierHistoryIdType(str, Enum):
    SESSION_ID = "session_id"
    TASK_ID = "task_id"

    def __str__(self) -> str:
        return str(self.value)
