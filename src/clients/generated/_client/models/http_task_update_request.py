from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.http_task_update_request_status import HttpTaskUpdateRequestStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_task_update_request_details import HttpTaskUpdateRequestDetails


T = TypeVar("T", bound="HttpTaskUpdateRequest")


@_attrs_define
class HttpTaskUpdateRequest:
    """
    Attributes:
        current_action (str):
        jira_ticket (str):
        message (str):
        session_id (str):
        status (HttpTaskUpdateRequestStatus):
        details (HttpTaskUpdateRequestDetails | Unset):
        progress_percentage (float | Unset):
        timestamp (str | Unset):
    """

    current_action: str
    jira_ticket: str
    message: str
    session_id: str
    status: HttpTaskUpdateRequestStatus
    details: HttpTaskUpdateRequestDetails | Unset = UNSET
    progress_percentage: float | Unset = UNSET
    timestamp: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_action = self.current_action

        jira_ticket = self.jira_ticket

        message = self.message

        session_id = self.session_id

        status = self.status.value

        details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.details, Unset):
            details = self.details.to_dict()

        progress_percentage = self.progress_percentage

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "current_action": current_action,
                "jira_ticket": jira_ticket,
                "message": message,
                "session_id": session_id,
                "status": status,
            }
        )
        if details is not UNSET:
            field_dict["details"] = details
        if progress_percentage is not UNSET:
            field_dict["progress_percentage"] = progress_percentage
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_task_update_request_details import HttpTaskUpdateRequestDetails

        d = dict(src_dict)
        current_action = d.pop("current_action")

        jira_ticket = d.pop("jira_ticket")

        message = d.pop("message")

        session_id = d.pop("session_id")

        status = HttpTaskUpdateRequestStatus(d.pop("status"))

        _details = d.pop("details", UNSET)
        details: HttpTaskUpdateRequestDetails | Unset
        if isinstance(_details, Unset):
            details = UNSET
        else:
            details = HttpTaskUpdateRequestDetails.from_dict(_details)

        progress_percentage = d.pop("progress_percentage", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        http_task_update_request = cls(
            current_action=current_action,
            jira_ticket=jira_ticket,
            message=message,
            session_id=session_id,
            status=status,
            details=details,
            progress_percentage=progress_percentage,
            timestamp=timestamp,
        )

        http_task_update_request.additional_properties = d
        return http_task_update_request

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
