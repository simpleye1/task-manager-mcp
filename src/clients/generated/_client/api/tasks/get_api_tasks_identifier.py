from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_api_tasks_identifier_id_type import GetApiTasksIdentifierIdType
from ...models.http_error_response import HttpErrorResponse
from ...models.http_task_status_response import HttpTaskStatusResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    identifier: str,
    *,
    id_type: GetApiTasksIdentifierIdType | Unset = GetApiTasksIdentifierIdType.SESSION_ID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_id_type: str | Unset = UNSET
    if not isinstance(id_type, Unset):
        json_id_type = id_type.value

    params["id_type"] = json_id_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/tasks/{identifier}".format(
            identifier=quote(str(identifier), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HttpErrorResponse | HttpTaskStatusResponse | None:
    if response.status_code == 200:
        response_200 = HttpTaskStatusResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = HttpErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = HttpErrorResponse.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HttpErrorResponse | HttpTaskStatusResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identifier: str,
    *,
    client: AuthenticatedClient | Client,
    id_type: GetApiTasksIdentifierIdType | Unset = GetApiTasksIdentifierIdType.SESSION_ID,
) -> Response[HttpErrorResponse | HttpTaskStatusResponse]:
    """Get task status

     Get the current status of a task by identifier

    Args:
        identifier (str):
        id_type (GetApiTasksIdentifierIdType | Unset):  Default:
            GetApiTasksIdentifierIdType.SESSION_ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskStatusResponse]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        id_type=id_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    identifier: str,
    *,
    client: AuthenticatedClient | Client,
    id_type: GetApiTasksIdentifierIdType | Unset = GetApiTasksIdentifierIdType.SESSION_ID,
) -> HttpErrorResponse | HttpTaskStatusResponse | None:
    """Get task status

     Get the current status of a task by identifier

    Args:
        identifier (str):
        id_type (GetApiTasksIdentifierIdType | Unset):  Default:
            GetApiTasksIdentifierIdType.SESSION_ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskStatusResponse
    """

    return sync_detailed(
        identifier=identifier,
        client=client,
        id_type=id_type,
    ).parsed


async def asyncio_detailed(
    identifier: str,
    *,
    client: AuthenticatedClient | Client,
    id_type: GetApiTasksIdentifierIdType | Unset = GetApiTasksIdentifierIdType.SESSION_ID,
) -> Response[HttpErrorResponse | HttpTaskStatusResponse]:
    """Get task status

     Get the current status of a task by identifier

    Args:
        identifier (str):
        id_type (GetApiTasksIdentifierIdType | Unset):  Default:
            GetApiTasksIdentifierIdType.SESSION_ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskStatusResponse]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        id_type=id_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identifier: str,
    *,
    client: AuthenticatedClient | Client,
    id_type: GetApiTasksIdentifierIdType | Unset = GetApiTasksIdentifierIdType.SESSION_ID,
) -> HttpErrorResponse | HttpTaskStatusResponse | None:
    """Get task status

     Get the current status of a task by identifier

    Args:
        identifier (str):
        id_type (GetApiTasksIdentifierIdType | Unset):  Default:
            GetApiTasksIdentifierIdType.SESSION_ID.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskStatusResponse
    """

    return (
        await asyncio_detailed(
            identifier=identifier,
            client=client,
            id_type=id_type,
        )
    ).parsed
