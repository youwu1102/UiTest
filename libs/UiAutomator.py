# -*- encoding:UTF-8 -*-
from uiautomator import Device
from uiautomator import AutomatorDeviceObject
from uiautomator import JsonRPCError


# http://xiaocong.github.io/slides/android-uiautomator-and-python/#/first-usage
class UiAutomator(AutomatorDeviceObject):
    def __init__(self, serial=None):
        self.device = Device(serial)

    def info(self):
        return self.device.info

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

    def scroll(self, vertical, forward, steps=100, **kwargs):
        print vertical
        print forward
        print kwargs
        return self.device(**kwargs).scroll(steps=steps)



if __name__ == '__main__':
    ui = UiAutomator('82a3bb73')
    print ui.info().get('currentPackageName')
    print 's'
    ui.dump('tmp.xml')
    import time
    print time.time()
    #ui.scroll(vertical=True, forward=True,text='s')
    print ui.click(text='hid')
