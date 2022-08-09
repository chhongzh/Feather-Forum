from sqlite3 import connect


class sqlliteCtx(object):
    def __init__(self, dataPath=None):
        self.handler = None
        self.path = dataPath

    def __enter__(self):
        if(not self.path):
            raise FileNotFoundError('File is not Found')
        self.handler = connect(self.path, check_same_thread=False)
        return self.handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handler.commit()
        self.handler.close()
        return True
