from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException


class RouterService:
    def __init__(self, url: str, token: str, allowed_devices: list[str]):
        self.url = url
        self.token = token
        self.allowed_devices = set(allowed_devices)

    def build_url(self, endpoint: str) -> str:
        return urljoin(self.url, endpoint)

    def make_request(self, endpoint: str = 'cstecgi.cgi', **kwargs) -> requests.Response:
        url = self.build_url(endpoint)
        params = kwargs.pop('params', {}) or {}
        params['token'] = self.token

        response = requests.post(url, params=params, timeout=10, **kwargs)
        response.raise_for_status()
        return response

    def get_connected_devices(self) -> list[dict]:
        try:
            resp = self.make_request(json={'topicurl': 'getOnlineMsg'})
            data = resp.json()
            return data
        except (RequestException, ValueError) as e:
            print(f"Ошибка при запросе к роутеру: {e}")
            return []

    def check_allowed(self) -> list[dict]:
        devices = self.get_connected_devices()
        return [
            d for d in devices
            if d.get('name') in self.allowed_devices or d.get('mac') in self.allowed_devices
        ]

    @classmethod
    def from_settings(cls):
        from conf import settings
        return cls(settings.ROUTER_URL, settings.ROUTER_TOKEN, settings.DEVICES_LIST)
