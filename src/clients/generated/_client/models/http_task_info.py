from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_task_info_details import HttpTaskInfoDetails


T = TypeVar("T", bound="HttpTaskInfo")


@_attrs_define
class HttpTaskInfo:
    """
    Attributes:
        created_at (str | Unset):
        current_action (str | Unset):
        details (HttpTaskInfoDetails | Unset):
        jira_ticket (str | Unset):
        message (str | Unset):
        progress_percentage (float | Unset):
        session_id (str | Unset):
        status (str | Unset):
        task_id (str | Unset):
        updated_at (str | Unset):
    """

    created_at: str | Unset = UNSET
    current_action: str | Unset = UNSET
    details: HttpTaskInfoDetails | Unset = UNSET
    jira_ticket: str | Unset = UNSET
    message: str | Unset = UNSET
    progress_percentage: float | Unset = UNSET
    session_id: str | Unset = UNSET
    status: str | Unset = UNSET
    task_id: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        current_action = self.current_action

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        jira_ticket = self.jira_ticket

        message = self.message

        progress_percentage = self.progress_percentage

        session_id = self.session_id

        status = self.status

        task_id = self.task_id

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if current_action is not UNSET:
            field_dict["current_action"] = current_action
        if details is not UNSET:
            field_dict["details"] = details
        if jira_ticket is not UNSET:
            field_dict["jira_ticket"] = jira_ticket
        if message is not UNSET:
            field_dict["message"] = message
        if progress_percentage is not UNSET:
            field_dict["progress_percentage"] = progress_percentage
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if status is not UNSET:
            field_dict["status"] = status
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_task_info_details import HttpTaskInfoDetails

        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        current_action = d.pop("current_action", UNSET)

        _details = d.pop("details", UNSET)
        details: HttpTaskInfoDetails | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = HttpTaskInfoDetails.from_dict(_details)

        jira_ticket = d.pop("jira_ticket", UNSET)

        message = d.pop("message", UNSET)

        progress_percentage = d.pop("progress_percentage", UNSET)

        session_id = d.pop("session_id", UNSET)

        status = d.pop("status", UNSET)

        task_id = d.pop("task_id", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        http_task_info = cls(
            created_at=created_at,
            current_action=current_action,
            details=details,
            jira_ticket=jira_ticket,
            message=message,
            progress_percentage=progress_percentage,
            session_id=session_id,
            status=status,
            task_id=task_id,
            updated_at=updated_at,
        )

        http_task_info.additional_properties = d
        return http_task_info

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
