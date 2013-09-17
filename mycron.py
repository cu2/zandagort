"""
Custom Cron (scheduler)

Check tasks at every <base_delay> seconds (can be float). Runs them when they should run (every <freq> checks).

Usage:
cron = MyCron(60) # check once a minute
cron.add_task("taskone", 5, testfun) # call testfun() every 5 minutes
cron.remove_task("taskone") # remove task (so it won't be executed anymore)

Inspiration:
http://stackoverflow.com/questions/373335/suggestions-for-a-cron-like-scheduler-in-python/374207#374207
"""


import datetime
import time
import threading


class MyCron(object):
    
    def __init__(self, base_delay=60.0):
        self.base_delay = base_delay
        self.tasks = {}
        self.last_check = datetime.datetime.now()
        self.checker_thread = threading.Thread(target=self.checker)
        self.checker_thread.daemon = True
    
    def add_task(self, name, freq, task, *args, **kwargs):
        self.tasks[name] = {
            "freq": freq,
            "counter": 0,
            "task": task,
            "args": args,
            "kwargs": kwargs,
        }
    
    def remove_task(self, name):
        if name in self.tasks:
            del self.tasks[name]
    
    def start(self):
        self.checker_thread.start()
    
    def checker(self):
        while True:
            self.last_check = datetime.datetime.now()
            for name in self.tasks:
                self.tasks[name]["counter"] += 1
                if self.tasks[name]["counter"] >= self.tasks[name]["freq"]:
                    self.tasks[name]["counter"] = 0
                    self.tasks[name]["task"](*self.tasks[name]["args"], **self.tasks[name]["kwargs"])
            now = datetime.datetime.now()
            if now >= self.last_check:
                seconds_since_last_check = 1.0 * (now - self.last_check).microseconds / 1000000
                if seconds_since_last_check < self.base_delay:
                    time.sleep(self.base_delay - seconds_since_last_check)
