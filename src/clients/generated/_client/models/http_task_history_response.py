from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_task_history_data import HttpTaskHistoryData


T = TypeVar("T", bound="HttpTaskHistoryResponse")


@_attrs_define
class HttpTaskHistoryResponse:
    """
    Attributes:
        data (HttpTaskHistoryData | Unset):
        success (bool | Unset):
    """

    data: HttpTaskHistoryData | Unset = UNSET
    success: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_task_history_data import HttpTaskHistoryData

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: HttpTaskHistoryData | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = HttpTaskHistoryData.from_dict(_data)

        success = d.pop("success", UNSET)

        http_task_history_response = cls(
            data=data,
            success=success,
        )

        http_task_history_response.additional_properties = d
        return http_task_history_response

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
