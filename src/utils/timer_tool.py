class CoolDown:
    def __init__(self, interval):
        self.interval = interval
        self.last = 0

    def get_interval(self):
        if callable(self.interval):
            return self.interval()
        return self.interval

    def ready(self, now):
        return now - self.last >= self.get_interval()

    def reset(self, now):
        self.last = now