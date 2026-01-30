from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_execution_info import HttpExecutionInfo


T = TypeVar("T", bound="HttpExecutionsData")


@_attrs_define
class HttpExecutionsData:
    """
    Attributes:
        executions (list[HttpExecutionInfo] | Unset):
        limit (int | Unset):
        page (int | Unset):
        total_count (int | Unset):
    """

    executions: list[HttpExecutionInfo] | Unset = UNSET
    limit: int | Unset = UNSET
    page: int | Unset = UNSET
    total_count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        executions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.executions, Unset):
            executions = []
            for executions_item_data in self.executions:
                executions_item = executions_item_data.to_dict()
                executions.append(executions_item)

        limit = self.limit

        page = self.page

        total_count = self.total_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if executions is not UNSET:
            field_dict["executions"] = executions
        if limit is not UNSET:
            field_dict["limit"] = limit
        if page is not UNSET:
            field_dict["page"] = page
        if total_count is not UNSET:
            field_dict["total_count"] = total_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.http_execution_info import HttpExecutionInfo

        d = dict(src_dict)
        _executions = d.pop("executions", UNSET)
        executions: list[HttpExecutionInfo] | Unset = UNSET
        if _executions is not UNSET:
            executions = []
            for executions_item_data in _executions:
                executions_item = HttpExecutionInfo.from_dict(executions_item_data)

                executions.append(executions_item)

        limit = d.pop("limit", UNSET)

        page = d.pop("page", UNSET)

        total_count = d.pop("total_count", UNSET)

        http_executions_data = cls(
            executions=executions,
            limit=limit,
            page=page,
            total_count=total_count,
        )

        http_executions_data.additional_properties = d
        return http_executions_data

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
