# ---------------------------------------------------------------------------
from time import time
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
class Cache(object):

    def __init__(self) -> None:
        self.data = {}
        self.expired = {}

    def setItem(self, itemName: str, item: object, expired: float = 0) -> None:
        self.checkExpired()
        self.data[itemName] = item
        if (expired > 0):
            self.expired[itemName] == expired

    def removeItem(self, itemName: str) -> None:
        self.checkExpired()
        try:
            self.data.pop(itemName)
        except:
            pass

    def getItem(self, itemName: str) -> None | object:
        self.checkExpired()
        if (self.searchItem(itemName)):
            return self.data[itemName]
        else:
            return None

    def searchItem(self, itemName: str) -> bool:
        self.checkExpired()
        if (itemName in self.data.copy().keys()):
            return True
        else:
            return False

    def clear(self) -> None:
        self.data.clear()

    def checkExpired(self) -> None:
        for key in self.expired.copy().keys():
            if (time() > self.expired[key] and self.expired[key] is not None):
                self.expired.pop(key)
                self.data.pop(key)
# ---------------------------------------------------------------------------
