from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_error_response import HttpErrorResponse
from ...models.http_patch_step_request import HttpPatchStepRequest
from ...models.http_step_response import HttpStepResponse
from ...types import Response


def _get_kwargs(
    execution_id: str,
    step_id: str,
    *,
    body: HttpPatchStepRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/executions/{execution_id}/steps/{step_id}".format(
            execution_id=quote(str(execution_id), safe=""),
            step_id=quote(str(step_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HttpErrorResponse | HttpStepResponse | None:
    if response.status_code == 200:
        response_200 = HttpStepResponse.from_dict(response.json())

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
) -> Response[HttpErrorResponse | HttpStepResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    execution_id: str,
    step_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: HttpPatchStepRequest,
) -> Response[HttpErrorResponse | HttpStepResponse]:
    """Partially update step

     Partially update an execution step (only provided fields are updated)

    Args:
        execution_id (str):
        step_id (str):
        body (HttpPatchStepRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpStepResponse]
    """

    kwargs = _get_kwargs(
        execution_id=execution_id,
        step_id=step_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    execution_id: str,
    step_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: HttpPatchStepRequest,
) -> HttpErrorResponse | HttpStepResponse | None:
    """Partially update step

     Partially update an execution step (only provided fields are updated)

    Args:
        execution_id (str):
        step_id (str):
        body (HttpPatchStepRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpStepResponse
    """

    return sync_detailed(
        execution_id=execution_id,
        step_id=step_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    execution_id: str,
    step_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: HttpPatchStepRequest,
) -> Response[HttpErrorResponse | HttpStepResponse]:
    """Partially update step

     Partially update an execution step (only provided fields are updated)

    Args:
        execution_id (str):
        step_id (str):
        body (HttpPatchStepRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HttpErrorResponse | HttpStepResponse]
    """

    kwargs = _get_kwargs(
        execution_id=execution_id,
        step_id=step_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    execution_id: str,
    step_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: HttpPatchStepRequest,
) -> HttpErrorResponse | HttpStepResponse | None:
    """Partially update step

     Partially update an execution step (only provided fields are updated)

    Args:
        execution_id (str):
        step_id (str):
        body (HttpPatchStepRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HttpErrorResponse | HttpStepResponse
    """

    return (
        await asyncio_detailed(
            execution_id=execution_id,
            step_id=step_id,
            client=client,
            body=body,
        )
    ).parsed
