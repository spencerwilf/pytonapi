import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp
from aiohttp import ClientResponse, ContentTypeError

from pytonapi.exceptions import (TONAPIBadRequestError,
                                 TONAPIError, TONAPIInternalServerError,
                                 TONAPINotFoundError, TONAPIUnauthorizedError,
                                 TONAPITooManyRequestsError)


class AsyncTonapiClient:

    def __init__(self, api_key: str, testnet: bool = False, max_retries: int = 3):
        self._api_key = api_key
        self._testnet = testnet
        self._max_retries = max_retries

        self.__headers = {'Authorization': f'Bearer {api_key}'}
        self.__base_url = "https://testnet.tonapi.io/" if testnet else "https://tonapi.io/"

    @staticmethod
    async def __process_response(response: ClientResponse) -> Any:
        status_code = response.status

        try:
            response = await response.json()
            error = response.get('error', response)
        except ContentTypeError:
            error = await response.text()
            response = True if status_code == 200 else False

        if status_code == 200:
            return response
        elif status_code == 400:
            raise TONAPIBadRequestError(error)
        elif status_code == 401:
            raise TONAPIUnauthorizedError
        elif status_code == 404:
            raise TONAPINotFoundError
        elif status_code == 429:
            raise TONAPITooManyRequestsError(error)
        elif status_code == 500:
            raise TONAPIInternalServerError(error)
        else:
            raise TONAPIError(error)

    async def __retry(self, request: callable, *args, **kwargs):
        for i in range(self._max_retries):
            try:
                async with request(*args, **kwargs) as response:
                    return await self.__process_response(response)
            except TONAPITooManyRequestsError:
                logging.warning(
                    f"Rate limit exceeded. Retrying "
                    f"{i + 1}/{self._max_retries} is in progress."
                )
                await asyncio.sleep(1)
        raise TONAPITooManyRequestsError

    async def _get(self, method: str, params: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, Any]] = None,
                   ) -> Dict[str, Any]:
        """
        Send a GET request to the TONAPI.

        :param method: The API method to call.
        :param params: The query parameters to include in the request.
        :param headers: The headers to include in the request.
        :return: The response data.

        :raises TONAPIBadRequestError: Raised when the client sends a bad request (HTTP 400).
        :raises TONAPIUnauthorizedError: Raised when the client is not authorized to access a resource (HTTP 401).
        :raises TONAPINotFoundError: Raised when the requested resource is not found (HTTP 404).
        :raises TONAPITooManyRequestsError: Raised when the rate limit is exceeded (HTTP 429).
        :raises TONAPIInternalServerError: Raised when the server encounters an internal error (HTTP 500).
        :raises TONAPIError: Raised when the response contains an error.
        """
        params = params.copy() if params else {}
        headers.update(self.__headers) if headers else ...
        headers = headers or self.__headers

        async with aiohttp.ClientSession(headers=headers) as session:
            url = f"{self.__base_url}{method}"
            return await self.__retry(session.get, url=url, params=params, ssl=False)

    async def _post(self, method: str, body: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, Any]] = None
                    ) -> Dict[str, Any]:
        """
        Send a POST request to the TONAPI.

        :param method: The API method to call.
        :param body: The request parameters to include in the request body.
        :param headers: The headers to include in the request.
        :return: The response data.

        :raises TONAPIBadRequestError: Raised when the client sends a bad request (HTTP 400).
        :raises TONAPIUnauthorizedError: Raised when the client is not authorized to access a resource (HTTP 401).
        :raises TONAPINotFoundError: Raised when the requested resource is not found (HTTP 404).
        :raises TONAPITooManyRequestsError: Raised when the rate limit is exceeded (HTTP 429).
        :raises TONAPIInternalServerError: Raised when the server encounters an internal error (HTTP 500).
        :raises TONAPIError: Raised when the response contains an error.
        """
        body = body.copy() if body else {}
        headers.update(self.__headers) if headers else ...
        headers = headers or self.__headers

        async with aiohttp.ClientSession(headers=headers) as session:
            url = f"{self.__base_url}{method}"
            return await self.__retry(session.post, url=url, json=body, ssl=False)
