# -*- encoding:UTF-8 -*-
from uiautomator import Device
from uiautomator import AutomatorDeviceObject
from uiautomator import JsonRPCError
from uiautomator import Selector

# http://xiaocong.github.io/slides/android-uiautomator-and-python/#/first-usage
class UiAutomator(AutomatorDeviceObject):
    def __init__(self, serial=None):
        self.device = Device(serial)

    def info(self):
        return self.device.info()

    def dump(self, filename=None, compressed=True, pretty=True):
        return self.device.dump(filename=filename, compressed=compressed, pretty=pretty)

    def click(self, **kwargs):
        try:
            return self.device(**kwargs).click()
        except JsonRPCError, e:
            return e

    def long_click(self, **kwargs):
        try:
            return self.device(**kwargs).long_click()
        except JsonRPCError, e:
            return e

    def scroll(self,vertical,forward,steps=100,**kwargs):
        return self.device(**kwargs).scroll()

if __name__ == '__main__':
    ui = UiAutomator()
    import time
    print time.time()
    ui.scroll(vertical=True,forward=True,text='sss')
