from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpDashboardHealthResponse")


@_attrs_define
class HttpDashboardHealthResponse:
    """
    Attributes:
        avg_latency_ms (float | Unset):
        cpu_percent (float | Unset):
        memory_percent (float | Unset):
        memory_used_mb (float | Unset):
        status (str | Unset):
        timestamp (str | Unset):
    """

    avg_latency_ms: float | Unset = UNSET
    cpu_percent: float | Unset = UNSET
    memory_percent: float | Unset = UNSET
    memory_used_mb: float | Unset = UNSET
    status: str | Unset = UNSET
    timestamp: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avg_latency_ms = self.avg_latency_ms

        cpu_percent = self.cpu_percent

        memory_percent = self.memory_percent

        memory_used_mb = self.memory_used_mb

        status = self.status

        timestamp = self.timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avg_latency_ms is not UNSET:
            field_dict["avg_latency_ms"] = avg_latency_ms
        if cpu_percent is not UNSET:
            field_dict["cpu_percent"] = cpu_percent
        if memory_percent is not UNSET:
            field_dict["memory_percent"] = memory_percent
        if memory_used_mb is not UNSET:
            field_dict["memory_used_mb"] = memory_used_mb
        if status is not UNSET:
            field_dict["status"] = status
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        avg_latency_ms = d.pop("avg_latency_ms", UNSET)

        cpu_percent = d.pop("cpu_percent", UNSET)

        memory_percent = d.pop("memory_percent", UNSET)

        memory_used_mb = d.pop("memory_used_mb", UNSET)

        status = d.pop("status", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        http_dashboard_health_response = cls(
            avg_latency_ms=avg_latency_ms,
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_used_mb=memory_used_mb,
            status=status,
            timestamp=timestamp,
        )

        http_dashboard_health_response.additional_properties = d
        return http_dashboard_health_response

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
