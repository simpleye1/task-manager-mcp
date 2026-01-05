from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpErrorResponse")


@_attrs_define
class HttpErrorResponse:
    """
    Attributes:
        error (str | Unset):
        error_code (str | Unset):
        success (bool | Unset):
        timestamp (str | Unset):
    """

    error: str | Unset = UNSET
    error_code: str | Unset = UNSET
    success: bool | Unset = UNSET
    timestamp: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        error_code = self.error_code

        success = self.success

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if success is not UNSET:
            field_dict["success"] = success
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        error = d.pop("error", UNSET)

        error_code = d.pop("error_code", UNSET)

        success = d.pop("success", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        http_error_response = cls(
            error=error,
            error_code=error_code,
            success=success,
            timestamp=timestamp,
        )

        http_error_response.additional_properties = d
        return http_error_response

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
