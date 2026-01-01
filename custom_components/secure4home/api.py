"""API Client for Secure4Home."""
import logging
from typing import Any

import aiohttp

from .const import API_BASE_URL

_LOGGER = logging.getLogger(__name__)


class Secure4HomeAPI:
    """API Client for Secure4Home."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize the API client."""
        self.username = username
        self.password = password
        self.token: str | None = None
        self.session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self) -> None:
        """Close the session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        require_auth: bool = True,
    ) -> dict[str, Any]:
        """Make API request."""
        session = await self._get_session()
        url = f"{API_BASE_URL}{endpoint}"

        headers = {}
        if require_auth and self.token:
            headers["token"] = self.token

        _LOGGER.debug("API Request: %s %s", method, url)

        async with session.request(
            method, url, json=data, headers=headers
        ) as response:
            response.raise_for_status()
            result = await response.json()
            _LOGGER.debug("API Response: %s", result)
            return result

    async def login(self) -> bool:
        """Login to Secure4Home API."""
        try:
            data = {"account": self.username, "password": self.password}
            response = await self._request(
                "POST", "auth/login", data=data, require_auth=False
            )

            # Extract token from response
            # API uses "token" not "sToken"
            if "token" in response:
                self.token = response["token"]
                _LOGGER.info("Successfully logged in to Secure4Home")
                return True
            else:
                _LOGGER.error("No token in login response: %s", response.keys())
                return False

        except Exception as err:
            _LOGGER.error("Login failed: %s", err)
            raise

    async def get_panel_area(self) -> dict[str, Any]:
        """Get panel area configuration."""
        return await self._request("GET", "panel/area")

    async def get_panel_status(self) -> dict[str, Any]:
        """Get panel status (system health - battery, tamper, etc)."""
        return await self._request("GET", "panel/status")

    async def get_panel_mode(self) -> dict[str, Any]:
        """Get panel mode (current arm/disarm state)."""
        return await self._request("GET", "panel/mode")

    async def set_panel_mode(
        self, area: str, mode: str, pincode: str
    ) -> dict[str, Any]:
        """Set panel mode (arm/disarm/home)."""
        data = {"area": area, "mode": mode, "pincode": pincode}
        return await self._request("POST", "panel/mode", data=data)

    async def get_user_info(self) -> dict[str, Any]:
        """Get user information."""
        return await self._request("POST", "user/info")

    async def get_device_history(self, params: dict[str, Any]) -> dict[str, Any]:
        """Get device history."""
        return await self._request("GET", "device/history", data=params)

    async def extend_token(self) -> bool:
        """Extend authentication token."""
        try:
            await self._request("GET", "auth/extend")
            return True
        except Exception as err:
            _LOGGER.error("Token extend failed: %s", err)
            return False

    async def logout(self) -> bool:
        """Logout from Secure4Home API."""
        try:
            await self._request("POST", "auth/logout")
            self.token = None
            return True
        except Exception as err:
            _LOGGER.error("Logout failed: %s", err)
            return False
