# trello_api.py
import httpx

TRELLO_API_BASE = "https://api.trello.com/1"

class TrelloClient:
    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
        self.base_url = TRELLO_API_BASE
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def close(self):
        await self.client.aclose()

    async def _get(self, endpoint: str, params: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)
        try:
            response = await self.client.get(endpoint, params=all_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            raise
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            raise

    async def _post(self, endpoint: str, data: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        try:
            response = await self.client.post(endpoint, params=all_params, 
                                              json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            raise
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            raise

    async def _put(self, endpoint: str, data: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        try:
            response = await self.client.put(endpoint, params=all_params, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            raise
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            raise

    async def _delete(self, endpoint: str, params: dict = None):
        all_params = {"key": self.api_key, "token": self.token}
        if params:
            all_params.update(params)
        try:
            response = await self.client.delete(endpoint, params=all_params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            raise
        except httpx.RequestError as e:
            print(f"Request error: {e}")
            raise
