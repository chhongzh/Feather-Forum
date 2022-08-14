from sqlite3 import connect


class Sqlite(object):
    def __init__(self, path, **kwargs):
        from sqlite3 import connect
        self.c = None
        self.path = path
        self.kwargs = kwargs

    def __enter__(self):
        self.c = connect(self.path, **self.kwargs)
        self.conn = self.c.cursor()
        return self.c, self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.c.commit()
        self.c.close()
