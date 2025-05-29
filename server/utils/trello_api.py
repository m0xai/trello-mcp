# trello_api.py
import logging
import asyncio
import os

import httpx

# Configure logging
logger = logging.getLogger(__name__)

TRELLO_API_BASE = "https://api.trello.com/1"


def trello_rate_limit_handler(func):
    async def wrapper(self, *args, **kwargs):
        max_retries = 5
        delay = 2  # seconds
        for attempt in range(max_retries):
            try:
                response = await func(self, *args, **kwargs)
                return response
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    logger.warning(f"Trello rate limit hit. Attempt {attempt+1}/{max_retries}. Backing off...")
                    # Try to get retry-after header, otherwise use delay
                    retry_after = e.response.headers.get("Retry-After")
                    if retry_after:
                        wait_time = int(retry_after)
                    else:
                        wait_time = delay * (2 ** attempt)  # exponential backoff
                    await asyncio.sleep(wait_time)
                    continue
                raise
        logger.error("Exceeded maximum retries due to Trello rate limiting.")
        raise Exception("Trello API rate limit exceeded. Please try again later.")
    return wrapper


def redact_sensitive(data):
    if isinstance(data, dict):
        data = data.copy()
        if 'token' in data:
            data['token'] = '***REDACTED***'
        if 'key' in data:
            data['key'] = '***REDACTED***'
    return data


class TrelloClient:
    """
    Client class for interacting with the Trello API over REST.
    """

    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
        self.base_url = TRELLO_API_BASE
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def close(self):
        await self.client.aclose()

    @trello_rate_limit_handler
    async def GET(self, endpoint: str, params: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)
        try:
            response = await self.client.get(endpoint, params=all_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                headers = getattr(e.response, "headers", {})
                print("WWW-Authenticate header:", headers.get("WWW-Authenticate"))
                api_key = os.getenv("TRELLO_API_KEY", self.api_key)
                auth_url = f"https://trello.com/1/authorize?expiration=never&name=Trello+Assistant+MCP&scope=read,write&response_type=token&key={api_key}"
                logger.info(f"Trello authorization required. Please visit this URL to authorize the app: {auth_url}")
            logger.error(f"HTTP error: {e} | endpoint: {endpoint} | params: {redact_sensitive(all_params)}")
            raise httpx.HTTPStatusError(
                f"Failed to get {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e} | endpoint: {endpoint} | params: {redact_sensitive(all_params)}")
            raise httpx.RequestError(f"Failed to get {endpoint}: {str(e)}")

    @trello_rate_limit_handler
    async def POST(self, endpoint: str, data: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        try:
            response = await self.client.post(endpoint, params=all_params, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                headers = getattr(e.response, "headers", {})
                print("WWW-Authenticate header:", headers.get("WWW-Authenticate"))
                api_key = os.getenv("TRELLO_API_KEY", self.api_key)
                auth_url = f"https://trello.com/1/authorize?expiration=never&name=Trello+Assistant+MCP&scope=read,write&response_type=token&key={api_key}"
                logger.info(f"Trello authorization required. Please visit this URL to authorize the app: {auth_url}")
            logger.error(f"HTTP error: {e} | endpoint: {endpoint} | params: {redact_sensitive(all_params)}")
            raise httpx.HTTPStatusError(
                f"Failed to post to {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e} | endpoint: {endpoint} | params: {redact_sensitive(all_params)}")
            raise httpx.RequestError(f"Failed to post to {endpoint}: {str(e)}")

    @trello_rate_limit_handler
    async def PUT(self, endpoint: str, data: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        try:
            response = await self.client.put(endpoint, params=all_params, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                headers = getattr(e.response, "headers", {})
                print("WWW-Authenticate header:", headers.get("WWW-Authenticate"))
                api_key = os.getenv("TRELLO_API_KEY", self.api_key)
                auth_url = f"https://trello.com/1/authorize?expiration=never&name=Trello+Assistant+MCP&scope=read,write&response_type=token&key={api_key}"
                logger.info(f"Trello authorization required. Please visit this URL to authorize the app: {auth_url}")
            logger.error(f"HTTP error: {e} | endpoint: {endpoint} | params: {redact_sensitive(all_params)}")
            raise httpx.HTTPStatusError(
                f"Failed to put to {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e} | endpoint: {endpoint} | params: {redact_sensitive(all_params)}")
            raise httpx.RequestError(f"Failed to put to {endpoint}: {str(e)}")

    @trello_rate_limit_handler
    async def DELETE(self, endpoint: str, params: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)
        try:
            response = await self.client.delete(endpoint, params=all_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                headers = getattr(e.response, "headers", {})
                print("WWW-Authenticate header:", headers.get("WWW-Authenticate"))
                api_key = os.getenv("TRELLO_API_KEY", self.api_key)
                auth_url = f"https://trello.com/1/authorize?expiration=never&name=Trello+Assistant+MCP&scope=read,write&response_type=token&key={api_key}"
                logger.info(f"Trello authorization required. Please visit this URL to authorize the app: {auth_url}")
            logger.error(f"HTTP error: {e} | endpoint: {endpoint} | params: {redact_sensitive(all_params)}")
            raise httpx.HTTPStatusError(
                f"Failed to delete {endpoint}: {str(e)}",
                request=e.request,
                response=e.response,
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {e} | endpoint: {endpoint} | params: {redact_sensitive(all_params)}")
            raise httpx.RequestError(f"Failed to delete {endpoint}: {str(e)}")
