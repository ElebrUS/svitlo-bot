from urllib.parse import urljoin
from hashlib import md5

import requests
from requests.exceptions import RequestException


class RouterService:
    def __init__(self, url: str, username: str, password: str, allowed_devices: list[str]):
        self.url = url
        self.username = username
        self.password = password
        self.allowed_devices = set(allowed_devices)
        self._token: str | None = None

    @property
    def token(self) -> str:
        if not self._token:
            self._token = self.get_token()
        return self._token

    def build_url(self, endpoint: str) -> str:
        return urljoin(self.url, endpoint)

    def get_token(self) -> str:
        resp = self.make_request(
            with_token=False,
            json={
                'topicurl': 'loginAuth',
                'username': md5(self.username.encode()).hexdigest(),
                'password': md5(self.password.encode()).hexdigest()
            }
        )
        resp.raise_for_status()
        data = resp.json()
        return data['jump_page'].split('?token=')[-1]

    def make_request(self, endpoint: str = 'cstecgi.cgi', with_token: bool = True, **kwargs) -> requests.Response:
        url = self.build_url(endpoint)
        params = kwargs.pop('params', {}) or {}
        if with_token:
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
        return cls(settings.ROUTER_URL, settings.ROUTER_USERNAME, settings.ROUTER_PASSWORD, settings.DEVICES_LIST)
