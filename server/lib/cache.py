from time import time


class Cache(object):

    def __init__(self):
        self.data = {}
        self.expired = {}

    def setItem(self, itemName: str, item: object, expired: float = 0):
        self.checkExpired()
        self.data[itemName] = item
        self.expired[itemName] = None if expired == 0 else expired+time()

    def removeItem(self, itemName):
        self.checkExpired()
        try:
            self.data.pop(itemName)
        except:
            pass

    def getItem(self, itemName):
        self.checkExpired()
        if(self.searchItem(itemName)):
            return self.data[itemName]
        else:
            return None

    def searchItem(self, itemName):
        self.checkExpired()
        if(itemName in self.data.copy().keys()):
            return True
        else:
            return False

    def clear(self):
        self.data.clear()

    def checkExpired(self):
        for key in self.data.copy().keys():
            if(time() > self.expired[key] and self.expired[key] is not None):
                self.expired.pop(key)
                self.data.pop(key)
