from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpLogsData")


@_attrs_define
class HttpLogsData:
    """
    Attributes:
        lines (int | Unset):
        logs (list[str] | Unset):
        total_lines (int | Unset):
    """

    lines: int | Unset = UNSET
    logs: list[str] | Unset = UNSET
    total_lines: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lines = self.lines

        logs: list[str] | Unset = UNSET
        if not isinstance(self.logs, Unset):
            logs = self.logs

        total_lines = self.total_lines

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lines is not UNSET:
            field_dict["lines"] = lines
        if logs is not UNSET:
            field_dict["logs"] = logs
        if total_lines is not UNSET:
            field_dict["total_lines"] = total_lines

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lines = d.pop("lines", UNSET)

        logs = cast(list[str], d.pop("logs", UNSET))

        total_lines = d.pop("total_lines", UNSET)

        http_logs_data = cls(
            lines=lines,
            logs=logs,
            total_lines=total_lines,
        )

        http_logs_data.additional_properties = d
        return http_logs_data

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
