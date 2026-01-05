from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_log_entry import HttpLogEntry
    from ..models.http_task_history_entry import HttpTaskHistoryEntry
    from ..models.http_task_info import HttpTaskInfo


T = TypeVar("T", bound="HttpTaskHistoryData")


@_attrs_define
class HttpTaskHistoryData:
    """
    Attributes:
        logs (list[HttpLogEntry] | Unset):
        status_history (list[HttpTaskHistoryEntry] | Unset):
        task_info (HttpTaskInfo | Unset):
    """

    logs: list[HttpLogEntry] | Unset = UNSET
    status_history: list[HttpTaskHistoryEntry] | Unset = UNSET
    task_info: HttpTaskInfo | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.logs, Unset):
            logs = []
            for logs_item_data in self.logs:
                logs_item = logs_item_data.to_dict()
                logs.append(logs_item)

        status_history: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.status_history, Unset):
            status_history = []
            for status_history_item_data in self.status_history:
                status_history_item = status_history_item_data.to_dict()
                status_history.append(status_history_item)

        task_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.task_info, Unset):
            task_info = self.task_info.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if logs is not UNSET:
            field_dict["logs"] = logs
        if status_history is not UNSET:
            field_dict["status_history"] = status_history
        if task_info is not UNSET:
            field_dict["task_info"] = task_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_log_entry import HttpLogEntry
        from ..models.http_task_history_entry import HttpTaskHistoryEntry
        from ..models.http_task_info import HttpTaskInfo

        d = dict(src_dict)
        _logs = d.pop("logs", UNSET)
        logs: list[HttpLogEntry] | Unset = UNSET
        if _logs is not UNSET:
            logs = []
            for logs_item_data in _logs:
                logs_item = HttpLogEntry.from_dict(logs_item_data)

                logs.append(logs_item)

        _status_history = d.pop("status_history", UNSET)
        status_history: list[HttpTaskHistoryEntry] | Unset = UNSET
        if _status_history is not UNSET:
            status_history = []
            for status_history_item_data in _status_history:
                status_history_item = HttpTaskHistoryEntry.from_dict(status_history_item_data)

                status_history.append(status_history_item)

        _task_info = d.pop("task_info", UNSET)
        task_info: HttpTaskInfo | Unset
        if isinstance(_task_info, Unset):
            task_info = UNSET
        else:
            task_info = HttpTaskInfo.from_dict(_task_info)

        http_task_history_data = cls(
            logs=logs,
            status_history=status_history,
            task_info=task_info,
        )

        http_task_history_data.additional_properties = d
        return http_task_history_data

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
