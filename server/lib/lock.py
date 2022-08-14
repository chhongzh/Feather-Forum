class Lock(object):
    def __init__(self):
        self.lock = False

    def release(self):
        self.lock = False

    def acquire(self):
        while(self.lock):
            pass
        self.lock = True
        return True

    def getLock(self):
        return self.lock
