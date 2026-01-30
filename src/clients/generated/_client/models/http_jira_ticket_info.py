from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpJIRATicketInfo")


@_attrs_define
class HttpJIRATicketInfo:
    """
    Attributes:
        assignee (str | Unset):
        description (str | Unset):
        key (str | Unset):
        reporter (str | Unset):
        status (str | Unset):
        summary (str | Unset):
    """

    assignee: str | Unset = UNSET
    description: str | Unset = UNSET
    key: str | Unset = UNSET
    reporter: str | Unset = UNSET
    status: str | Unset = UNSET
    summary: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        assignee = self.assignee

        description = self.description

        key = self.key

        reporter = self.reporter

        status = self.status

        summary = self.summary

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if description is not UNSET:
            field_dict["description"] = description
        if key is not UNSET:
            field_dict["key"] = key
        if reporter is not UNSET:
            field_dict["reporter"] = reporter
        if status is not UNSET:
            field_dict["status"] = status
        if summary is not UNSET:
            field_dict["summary"] = summary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        assignee = d.pop("assignee", UNSET)

        description = d.pop("description", UNSET)

        key = d.pop("key", UNSET)

        reporter = d.pop("reporter", UNSET)

        status = d.pop("status", UNSET)

        summary = d.pop("summary", UNSET)

        http_jira_ticket_info = cls(
            assignee=assignee,
            description=description,
            key=key,
            reporter=reporter,
            status=status,
            summary=summary,
        )

        http_jira_ticket_info.additional_properties = d
        return http_jira_ticket_info

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
