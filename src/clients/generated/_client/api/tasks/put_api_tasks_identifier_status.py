from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_error_response import HttpErrorResponse
from ...models.http_task_update_request import HttpTaskUpdateRequest
from ...models.http_task_update_response import HttpTaskUpdateResponse
from ...models.put_api_tasks_identifier_status_id_type import PutApiTasksIdentifierStatusIdType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    identifier: str,
    *,
    body: HttpTaskUpdateRequest,
    id_type: PutApiTasksIdentifierStatusIdType | Unset = PutApiTasksIdentifierStatusIdType.SESSION_ID,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_id_type: str | Unset = UNSET
    if not isinstance(id_type, Unset):
        json_id_type = id_type.value

    params["id_type"] = json_id_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/tasks/{identifier}/status".format(
            identifier=quote(str(identifier), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HttpErrorResponse | HttpTaskUpdateResponse | None:
    if response.status_code == 200:
        response_200 = HttpTaskUpdateResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = HttpErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 404:
        response_404 = HttpErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 500:
        response_500 = HttpErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HttpErrorResponse | HttpTaskUpdateResponse]:
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
    body: HttpTaskUpdateRequest,
    id_type: PutApiTasksIdentifierStatusIdType | Unset = PutApiTasksIdentifierStatusIdType.SESSION_ID,
) -> Response[HttpErrorResponse | HttpTaskUpdateResponse]:
    """Update task status

     Update task status and create history record

    Args:
        identifier (str):
        id_type (PutApiTasksIdentifierStatusIdType | Unset):  Default:
            PutApiTasksIdentifierStatusIdType.SESSION_ID.
        body (HttpTaskUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskUpdateResponse]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        body=body,
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
    body: HttpTaskUpdateRequest,
    id_type: PutApiTasksIdentifierStatusIdType | Unset = PutApiTasksIdentifierStatusIdType.SESSION_ID,
) -> HttpErrorResponse | HttpTaskUpdateResponse | None:
    """Update task status

     Update task status and create history record

    Args:
        identifier (str):
        id_type (PutApiTasksIdentifierStatusIdType | Unset):  Default:
            PutApiTasksIdentifierStatusIdType.SESSION_ID.
        body (HttpTaskUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskUpdateResponse
    """

    return sync_detailed(
        identifier=identifier,
        client=client,
        body=body,
        id_type=id_type,
    ).parsed


async def asyncio_detailed(
    identifier: str,
    *,
    client: AuthenticatedClient | Client,
    body: HttpTaskUpdateRequest,
    id_type: PutApiTasksIdentifierStatusIdType | Unset = PutApiTasksIdentifierStatusIdType.SESSION_ID,
) -> Response[HttpErrorResponse | HttpTaskUpdateResponse]:
    """Update task status

     Update task status and create history record

    Args:
        identifier (str):
        id_type (PutApiTasksIdentifierStatusIdType | Unset):  Default:
            PutApiTasksIdentifierStatusIdType.SESSION_ID.
        body (HttpTaskUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpTaskUpdateResponse]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        body=body,
        id_type=id_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identifier: str,
    *,
    client: AuthenticatedClient | Client,
    body: HttpTaskUpdateRequest,
    id_type: PutApiTasksIdentifierStatusIdType | Unset = PutApiTasksIdentifierStatusIdType.SESSION_ID,
) -> HttpErrorResponse | HttpTaskUpdateResponse | None:
    """Update task status

     Update task status and create history record

    Args:
        identifier (str):
        id_type (PutApiTasksIdentifierStatusIdType | Unset):  Default:
            PutApiTasksIdentifierStatusIdType.SESSION_ID.
        body (HttpTaskUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpTaskUpdateResponse
    """

    return (
        await asyncio_detailed(
            identifier=identifier,
            client=client,
            body=body,
            id_type=id_type,
        )
    ).parsed
