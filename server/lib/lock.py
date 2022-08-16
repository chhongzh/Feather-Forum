from time import sleep


class Lock(object):
    def __init__(self):
        self.lock = False

    def release(self):
        self.lock = False

    def acquire(self):
        while (self.lock):
            sleep(1)
        self.lock = True
        return True

    def getLock(self):
        return self.lock
