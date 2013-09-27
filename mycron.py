"""
Custom Cron (scheduler)
"""

import datetime
import time
import threading


class MyCron(object):
    """
    Custom cron (scheduler) class
    
    Check tasks at every <base_delay> seconds (can be float). Runs them when they should run (every <freq> checks).
    
    Usage:
    cron = MyCron(60) # check once a minute
    cron.add_task("taskone", 5, testfun) # call testfun() every 5 minutes
    cron.remove_task("taskone") # remove task (so it won't be executed anymore)
    
    Inspiration:
    http://stackoverflow.com/questions/373335/suggestions-for-a-cron-like-scheduler-in-python/374207#374207
    """
    
    def __init__(self, base_delay=60.0):
        self._base_delay = base_delay
        self._tasks = {}
        self._last_check = datetime.datetime.now()
        self._checker_thread = threading.Thread(target=self._checker)
        self._checker_thread.daemon = True
    
    def add_task(self, name, freq, task, *args, **kwargs):
        """Add task to tasklist"""
        self._tasks[name] = {
            "freq": freq,
            "counter": 0,
            "task": task,
            "args": args,
            "kwargs": kwargs,
        }
    
    def remove_task(self, name):
        """Remove task from tasklist by name"""
        if name in self._tasks:
            del self._tasks[name]
    
    def start(self):
        """Start checker thread"""
        self._checker_thread.start()
    
    def _checker(self):
        """Main loop of checker thread"""
        while True:
            self._last_check = datetime.datetime.now()
            for name in self._tasks:
                self._tasks[name]["counter"] += 1
                if self._tasks[name]["counter"] >= self._tasks[name]["freq"]:
                    self._tasks[name]["counter"] = 0
                    self._tasks[name]["task"](*self._tasks[name]["args"], **self._tasks[name]["kwargs"])
            now = datetime.datetime.now()
            if now >= self._last_check:
                seconds_since_last_check = 1.0 * (now - self._last_check).microseconds / 1000000
                if seconds_since_last_check < self._base_delay:
                    time.sleep(self._base_delay - seconds_since_last_check)
