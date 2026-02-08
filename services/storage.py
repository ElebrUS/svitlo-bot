import json
import os


class Storage:
    _full_data: dict | None = None

    def __init__(self, file_path='data/storage.json'):
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property
    def full_data(self) -> dict:
        if self._full_data is None:
            self._full_data = self.load_full_data()
        return self._full_data

    @property
    def curr_state(self) -> str:
        return self.full_data.get("current_state", "unknown")

    @property
    def shutdown(self) -> list:
        return self.full_data.get("shutdown", [])

    @shutdown.setter
    def shutdown(self, value: list):
        self.full_data["shutdown"] = value

    @curr_state.setter
    def curr_state(self, value: str):
        self.full_data["current_state"] = value

    @property
    def counter(self) -> int:
        return self.full_data.get("counter", 0)

    @counter.setter
    def counter(self, value: int):
        self.full_data["counter"] = value

    @property
    def last_record(self) -> dict | None:
        return self.full_data.get("shutdown", [])[-1] if self.full_data.get("shutdown") else None

    @property
    def prev_record(self) -> dict | None:
        return self.full_data.get("shutdown", [])[-2] if len(self.full_data.get("shutdown", [])) > 1 else None

    def load_full_data(self) -> dict:
        if not os.path.exists(self.file_path):
            return {
                "current_state": "unknown",
                "counter": 0,
                "shutdown": []
            }
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"current_state": "unknown", "counter": 0, "shutdown": []}

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.full_data, f, indent=4, ensure_ascii=False)

    def add_record(self, record: dict, is_save: bool = False):
        self.shutdown.append(record)
        if is_save:
            self.save()
