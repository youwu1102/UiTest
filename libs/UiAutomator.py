# -*- encoding:UTF-8 -*-
from uiautomator import Device
from uiautomator import AutomatorDeviceObject
from uiautomator import JsonRPCError

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

    def scroll(self, **kwargs):
        self.device(**kwargs).scroll.horiz.forward(steps=50) # default vertically and forward
        # d().scroll.horiz.forward(steps=100)
        # d().scroll.vert.backward(steps=100)
        # d().scroll.horiz.toBeginning(steps=100, max_swipes=100)
        # d().scroll.vert.toEnd(steps=100)
        # d().scroll.horiz.to(text="Clock")

if __name__ == '__main__':
    ui = UiAutomator()
    import time
    print time.time()
    ui.dump('aaa.xml')
    print time.time()
    print ui.scroll(resourceId="com.android.launcher3:id/apps_list_view")