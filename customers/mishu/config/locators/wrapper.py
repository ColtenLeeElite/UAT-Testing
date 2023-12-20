from playwright.async_api._generated import Locator
import re

class WrappedLocator(Locator):
    def selector(self):
        res = re.search("selector=[\',\"](.+)[\',\"]", str(self))
        return res.group(1)

    
    
    
def patch_locator(locator: Locator) -> WrappedLocator:
    locator.__class__ = WrappedLocator
    return locator



class LocatorDescriptor:

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, obj_type=None):
        locator: Locator = getattr(obj, self.private_name)
        locator = patch_locator(locator)
        return locator

    def __set__(self, obj, value: Locator):
        setattr(obj, self.private_name, value)
