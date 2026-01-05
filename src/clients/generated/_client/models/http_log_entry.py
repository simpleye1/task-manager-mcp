from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpLogEntry")


@_attrs_define
class HttpLogEntry:
    """
    Attributes:
        created_at (str | Unset):
        id (int | Unset):
        log_level (str | Unset):
        log_message (str | Unset):
    """

    created_at: str | Unset = UNSET
    id: int | Unset = UNSET
    log_level: str | Unset = UNSET
    log_message: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at

        id = self.id

        log_level = self.log_level

        log_message = self.log_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if log_level is not UNSET:
            field_dict["log_level"] = log_level
        if log_message is not UNSET:
            field_dict["log_message"] = log_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = d.pop("created_at", UNSET)

        id = d.pop("id", UNSET)

        log_level = d.pop("log_level", UNSET)

        log_message = d.pop("log_message", UNSET)

        http_log_entry = cls(
            created_at=created_at,
            id=id,
            log_level=log_level,
            log_message=log_message,
        )

        http_log_entry.additional_properties = d
        return http_log_entry

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
