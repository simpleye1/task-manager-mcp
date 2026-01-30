from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_jira_ticket_info import HttpJIRATicketInfo


T = TypeVar("T", bound="HttpTaskInfo")


@_attrs_define
class HttpTaskInfo:
    """
    Attributes:
        created_at (str | Unset):
        failure_reason (str | Unset):
        jira_info (HttpJIRATicketInfo | Unset):
        jira_ticket_id (str | Unset):
        retry_count (int | Unset):
        status (str | Unset):
        task_id (str | Unset):
        updated_at (str | Unset):
    """

    created_at: str | Unset = UNSET
    failure_reason: str | Unset = UNSET
    jira_info: HttpJIRATicketInfo | Unset = UNSET
    jira_ticket_id: str | Unset = UNSET
    retry_count: int | Unset = UNSET
    status: str | Unset = UNSET
    task_id: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        failure_reason = self.failure_reason

        jira_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.jira_info, Unset):
            jira_info = self.jira_info.to_dict()

        jira_ticket_id = self.jira_ticket_id

        retry_count = self.retry_count

        status = self.status

        task_id = self.task_id

        updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if failure_reason is not UNSET:
            field_dict["failure_reason"] = failure_reason
        if jira_info is not UNSET:
            field_dict["jira_info"] = jira_info
        if jira_ticket_id is not UNSET:
            field_dict["jira_ticket_id"] = jira_ticket_id
        if retry_count is not UNSET:
            field_dict["retry_count"] = retry_count
        if status is not UNSET:
            field_dict["status"] = status
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_jira_ticket_info import HttpJIRATicketInfo

        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        failure_reason = d.pop("failure_reason", UNSET)

        _jira_info = d.pop("jira_info", UNSET)
        jira_info: HttpJIRATicketInfo | Unset
        if isinstance(_jira_info, Unset):
            jira_info = UNSET
        else:
            jira_info = HttpJIRATicketInfo.from_dict(_jira_info)

        jira_ticket_id = d.pop("jira_ticket_id", UNSET)

        retry_count = d.pop("retry_count", UNSET)

        status = d.pop("status", UNSET)

        task_id = d.pop("task_id", UNSET)

        updated_at = d.pop("updated_at", UNSET)

        http_task_info = cls(
            created_at=created_at,
            failure_reason=failure_reason,
            jira_info=jira_info,
            jira_ticket_id=jira_ticket_id,
            retry_count=retry_count,
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
