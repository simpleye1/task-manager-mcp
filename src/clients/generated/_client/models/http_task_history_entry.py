from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_task_history_entry_details import HttpTaskHistoryEntryDetails


T = TypeVar("T", bound="HttpTaskHistoryEntry")


@_attrs_define
class HttpTaskHistoryEntry:
    """
    Attributes:
        created_at (str | Unset):
        current_action (str | Unset):
        details (HttpTaskHistoryEntryDetails | Unset):
        id (int | Unset):
        message (str | Unset):
        progress_percentage (float | Unset):
        status (str | Unset):
    """

    created_at: str | Unset = UNSET
    current_action: str | Unset = UNSET
    details: HttpTaskHistoryEntryDetails | Unset = UNSET
    id: int | Unset = UNSET
    message: str | Unset = UNSET
    progress_percentage: float | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        current_action = self.current_action

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        id = self.id

        message = self.message

        progress_percentage = self.progress_percentage

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if current_action is not UNSET:
            field_dict["current_action"] = current_action
        if details is not UNSET:
            field_dict["details"] = details
        if id is not UNSET:
            field_dict["id"] = id
        if message is not UNSET:
            field_dict["message"] = message
        if progress_percentage is not UNSET:
            field_dict["progress_percentage"] = progress_percentage
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_task_history_entry_details import HttpTaskHistoryEntryDetails

        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        current_action = d.pop("current_action", UNSET)

        _details = d.pop("details", UNSET)
        details: HttpTaskHistoryEntryDetails | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = HttpTaskHistoryEntryDetails.from_dict(_details)

        id = d.pop("id", UNSET)

        message = d.pop("message", UNSET)

        progress_percentage = d.pop("progress_percentage", UNSET)

        status = d.pop("status", UNSET)

        http_task_history_entry = cls(
            created_at=created_at,
            current_action=current_action,
            details=details,
            id=id,
            message=message,
            progress_percentage=progress_percentage,
            status=status,
        )

        http_task_history_entry.additional_properties = d
        return http_task_history_entry

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
