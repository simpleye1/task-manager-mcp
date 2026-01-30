from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpExecutionInfo")


@_attrs_define
class HttpExecutionInfo:
    """
    Attributes:
        comment_id (int | Unset):
        commit_sha (str | Unset):
        completed_at (str | Unset):
        confidence_level (int | Unset):
        confidence_reason (str | Unset):
        cost_usd (float | Unset):
        error_message (str | Unset):
        execution_id (str | Unset):
        raw_output (str | Unset):
        sandbox_type (str | Unset):
        session_id (str | Unset):
        started_at (str | Unset):
        status (str | Unset):
        task_id (str | Unset):
        trigger_type (str | Unset):
        worktree_path (str | Unset):
    """

    comment_id: int | Unset = UNSET
    commit_sha: str | Unset = UNSET
    completed_at: str | Unset = UNSET
    confidence_level: int | Unset = UNSET
    confidence_reason: str | Unset = UNSET
    cost_usd: float | Unset = UNSET
    error_message: str | Unset = UNSET
    execution_id: str | Unset = UNSET
    raw_output: str | Unset = UNSET
    sandbox_type: str | Unset = UNSET
    session_id: str | Unset = UNSET
    started_at: str | Unset = UNSET
    status: str | Unset = UNSET
    task_id: str | Unset = UNSET
    trigger_type: str | Unset = UNSET
    worktree_path: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        comment_id = self.comment_id

        commit_sha = self.commit_sha

        completed_at = self.completed_at

        confidence_level = self.confidence_level

        confidence_reason = self.confidence_reason

        cost_usd = self.cost_usd

        error_message = self.error_message

        execution_id = self.execution_id

        raw_output = self.raw_output

        sandbox_type = self.sandbox_type

        session_id = self.session_id

        started_at = self.started_at

        status = self.status

        task_id = self.task_id

        trigger_type = self.trigger_type

        worktree_path = self.worktree_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if comment_id is not UNSET:
            field_dict["comment_id"] = comment_id
        if commit_sha is not UNSET:
            field_dict["commit_sha"] = commit_sha
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if confidence_level is not UNSET:
            field_dict["confidence_level"] = confidence_level
        if confidence_reason is not UNSET:
            field_dict["confidence_reason"] = confidence_reason
        if cost_usd is not UNSET:
            field_dict["cost_usd"] = cost_usd
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if execution_id is not UNSET:
            field_dict["execution_id"] = execution_id
        if raw_output is not UNSET:
            field_dict["raw_output"] = raw_output
        if sandbox_type is not UNSET:
            field_dict["sandbox_type"] = sandbox_type
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if status is not UNSET:
            field_dict["status"] = status
        if task_id is not UNSET:
            field_dict["task_id"] = task_id
        if trigger_type is not UNSET:
            field_dict["trigger_type"] = trigger_type
        if worktree_path is not UNSET:
            field_dict["worktree_path"] = worktree_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        comment_id = d.pop("comment_id", UNSET)

        commit_sha = d.pop("commit_sha", UNSET)

        completed_at = d.pop("completed_at", UNSET)

        confidence_level = d.pop("confidence_level", UNSET)

        confidence_reason = d.pop("confidence_reason", UNSET)

        cost_usd = d.pop("cost_usd", UNSET)

        error_message = d.pop("error_message", UNSET)

        execution_id = d.pop("execution_id", UNSET)

        raw_output = d.pop("raw_output", UNSET)

        sandbox_type = d.pop("sandbox_type", UNSET)

        session_id = d.pop("session_id", UNSET)

        started_at = d.pop("started_at", UNSET)

        status = d.pop("status", UNSET)

        task_id = d.pop("task_id", UNSET)

        trigger_type = d.pop("trigger_type", UNSET)

        worktree_path = d.pop("worktree_path", UNSET)

        http_execution_info = cls(
            comment_id=comment_id,
            commit_sha=commit_sha,
            completed_at=completed_at,
            confidence_level=confidence_level,
            confidence_reason=confidence_reason,
            cost_usd=cost_usd,
            error_message=error_message,
            execution_id=execution_id,
            raw_output=raw_output,
            sandbox_type=sandbox_type,
            session_id=session_id,
            started_at=started_at,
            status=status,
            task_id=task_id,
            trigger_type=trigger_type,
            worktree_path=worktree_path,
        )

        http_execution_info.additional_properties = d
        return http_execution_info

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
