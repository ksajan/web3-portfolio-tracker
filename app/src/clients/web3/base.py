from typing import Optional, Union

from pydantic import BaseModel
from requests import JSONDecodeError, Session

import app.src.loader as _config


class _config:
    HTTP_SESSION = _config.HTTP_SESSION


class BaseConnector(BaseModel):
    session: Session = _config.HTTP_SESSION


class BaseHTTPConnector(BaseConnector):

    def _make_get_request(
        self, url: str, headers=None, params=None
    ) -> dict | Exception:
        response = self.session.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}: {response.content}")

    def _make_post_request(
        self, url: str, payload: dict, headers=None
    ) -> dict | Exception:
        response = self.session.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}: {response.content}")

    def _make_put_request(
        self, url: str, payload: dict, headers=None
    ) -> dict | Exception:
        response = self.session.put(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}: {response.content}")

    def _make_delete_request(self, url: str, headers=None) -> dict | Exception:
        response = self.session.delete(url)
        if response.status_code == 200:
            try:
                if response.text.strip():  # Checks if response text is not empty
                    return response.json()
                else:
                    return None
            except JSONDecodeError:
                raise ValueError("Received unexpected response format from API")
        else:
            response.raise_for_status()  # Handle other HTTP errors
