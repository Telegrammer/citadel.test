from application.ports import Clock
from datetime import datetime


class TimestampClock(Clock):
    def now(self) -> datetime:
        return datetime.now(tz=None)
