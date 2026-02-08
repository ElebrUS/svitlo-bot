from datetime import datetime
from pytz import timezone


class MonitorService:
    def __init__(self, router, bot, storage, n_limit=3):
        self.router = router
        self.bot = bot
        self.storage = storage
        self.n_limit = n_limit
        self.timezone = timezone('Europe/Kiev')

    def run_check(self):
        counter = self.storage.counter

        allowed_now = self.router.check_allowed()
        is_active = len(allowed_now) > 0
        new_state = 'enabled' if is_active else 'disabled'

        if new_state == self.storage.curr_state:
            counter += 1
        else:
            counter = 1

        if self.storage.curr_state != new_state:
            self._handle_state_change(new_state)

        if counter == self.n_limit:
            self._send_message()

        self.storage.counter = counter
        self.storage.curr_state = new_state
        self.storage.save()

    def _handle_state_change(self, state):
        dt_now = datetime.now(tz=self.timezone)

        record = {
            "date": dt_now.date().isoformat(),
            "dt_check": dt_now.isoformat(),
            "state": state
        }

        self.storage.add_record(record)

    def _send_message(self):
        record = self.storage.last_record
        if not record:
            return
        curr_dt = datetime.fromisoformat(record['dt_check']).astimezone(self.timezone)
        prev_dt = datetime.fromisoformat(self.storage.prev_record['dt_check']).astimezone(self.timezone) if self.storage.prev_record else None
        delta = curr_dt - prev_dt if prev_dt else None
        hours = delta.total_seconds() // 3600 if delta else 0
        minutes = (delta.total_seconds() % 3600) // 60 if delta else 0
        tpl_data = {
            'time': curr_dt.strftime('%H:%M'),
            'duration': f"{int(hours)}год {int(minutes)}хв" if delta else '',
            'prev_time': prev_dt.strftime('(з %H:%M)') if prev_dt else ''
        }
        self.bot.send_template(record['state'], **tpl_data)
