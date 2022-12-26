"""
此文件属于Feather-Forum!
© 2022 chhongzh

缓存类
"""
from time import time


class Cache(object):

    def __init__(self) -> None:
        self.data = {}
        self.expired = {}

    def setItem(self, itemName: str, item: object, expired: float = 0) -> None:
        self.check_expired()
        self.data[itemName] = item
        if (expired > 0):
            self.expired[itemName] = expired

    def removeItem(self, itemName: str) -> None:
        self.check_expired()
        try:
            self.data.pop(itemName)
        except:
            pass

    def getItem(self, itemName: str) -> None | object:
        self.check_expired()
        if (self.searchItem(itemName)):
            return self.data[itemName]
        else:
            return None

    def searchItem(self, itemName: str) -> bool:
        self.check_expired()
        return itemName in self.data.copy().keys()

    def clear(self) -> None:
        self.data.clear()

    def check_expired(self) -> None:
        for key in self.expired.copy().keys():
            if (time() > self.expired[key] and self.expired[key] is not None):
                self.expired.pop(key)
                self.data.pop(key)
