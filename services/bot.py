import requests
from urllib.parse import urljoin

class BotService:
    def __init__(self, token: str, chat_id: str, template_dir: str):
        self.token = token
        self.chat_id = chat_id
        self.template_dir = template_dir
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def _build_url(self, method: str) -> str:
        return urljoin(self.base_url, method)

    def send_message(self, text: str, parse_mode: str = 'HTML') -> bool:
        url = self._build_url("sendMessage")
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Ошибка при отправке в Telegram: {e}")
            return False

    @classmethod
    def from_settings(cls):
        from conf import settings
        return cls(settings.BOT_TOKEN, settings.CHANNEL_CHAT_ID, settings.TEMPLATE_DIR)

    def render_template(self, template_name: str, **kwargs) -> str:
        file_path = self.template_dir / f"{template_name}.tpl"

        if not file_path.exists():
            return f"Error: Template {template_name} not found."

        with open(file_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        return template_content.format(**kwargs)

    def send_template(self, template_name: str, **kwargs):
        text = self.render_template(template_name, **kwargs)
        return self.send_message(text)
