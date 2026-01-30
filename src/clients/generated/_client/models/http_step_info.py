from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpStepInfo")


@_attrs_define
class HttpStepInfo:
    """
    Attributes:
        completed_at (str | Unset):
        execution_id (str | Unset):
        message (str | Unset):
        started_at (str | Unset):
        status (str | Unset): Optional, defaults to "running"
        step_id (str | Unset):
        step_name (str | Unset):
    """

    completed_at: str | Unset = UNSET
    execution_id: str | Unset = UNSET
    message: str | Unset = UNSET
    started_at: str | Unset = UNSET
    status: str | Unset = UNSET
    step_id: str | Unset = UNSET
    step_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        completed_at = self.completed_at

        execution_id = self.execution_id

        message = self.message

        started_at = self.started_at

        status = self.status

        step_id = self.step_id

        step_name = self.step_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if execution_id is not UNSET:
            field_dict["execution_id"] = execution_id
        if message is not UNSET:
            field_dict["message"] = message
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if status is not UNSET:
            field_dict["status"] = status
        if step_id is not UNSET:
            field_dict["step_id"] = step_id
        if step_name is not UNSET:
            field_dict["step_name"] = step_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        completed_at = d.pop("completed_at", UNSET)

        execution_id = d.pop("execution_id", UNSET)

        message = d.pop("message", UNSET)

        started_at = d.pop("started_at", UNSET)

        status = d.pop("status", UNSET)

        step_id = d.pop("step_id", UNSET)

        step_name = d.pop("step_name", UNSET)

        http_step_info = cls(
            completed_at=completed_at,
            execution_id=execution_id,
            message=message,
            started_at=started_at,
            status=status,
            step_id=step_id,
            step_name=step_name,
        )

        http_step_info.additional_properties = d
        return http_step_info

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
