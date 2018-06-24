# coding=utf-8
"""
How long is this taking
"""
import datetime


class Timer(object):
    """A simple timer class"""

    def __init__(self) -> None:
        self.split_start: datetime.datetime
        self.start_time: datetime.datetime
        self.stop_time: datetime.datetime

    def start(self) -> datetime.datetime:
        """Starts the timer"""
        self.start_time = datetime.datetime.now()
        return self.start_time

    def stop(self, message: str = "Total: ") -> str:
        """Stops the timer.  Returns the time elapsed"""
        self.stop_time = datetime.datetime.now()
        return message + str(self.stop_time - self.start_time)

    def now(self, message: str = "Now: ") -> str:
        """Returns the current time with a message"""
        return message + ": " + str(datetime.datetime.now())

    def elapsed(self, message: str = "Elapsed: ") -> str:
        """Time elapsed since start was called"""
        return message + " " + str(datetime.datetime.now() - self.start_time)

    def split(self, message: str = "Split started at: ") -> str:
        """Start a split timer"""
        self.split_start = datetime.datetime.now()
        return message + str(self.split_start)

    def unsplit(self, message: str = "Unsplit: ") -> str:
        """Stops a split. Returns the time elapsed since split was called"""
        return message + str(datetime.datetime.now() - self.split_start)
