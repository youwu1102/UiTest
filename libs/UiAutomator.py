# -*- encoding:UTF-8 -*-
from uiautomator import Device
from uiautomator import AutomatorDeviceObject
from uiautomator import JsonRPCError


# http://xiaocong.github.io/slides/android-uiautomator-and-python/#/first-usage
class UiAutomator(object):
    def __init__(self, serial=None):
        self.device = Device(serial)

    def info(self):
        return self.device.info

    def dump(self, filename=None, compressed=True, pretty=True):
        return self.device.dump(filename=filename, compressed=compressed, pretty=pretty)

    def screenshot(self, filename, scale=1.0, quality=100):
        return self.device.screenshot(filename=filename, scale=scale, quality=quality)

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

    def get_current_package_name(self):
        return self.device.info.get('currentPackageName')


        # press key via name or key code. Supported key name includes:
        # home, back, left, right, up, down, center, menu, search, enter,
        # delete(or del), recent(recent apps), volume_up, volume_down,
        # volume_mute, camera, power.
        # Usage:
        # d.press.back()  # press back key
        # d.press.menu()  # press home key
        # d.press(89)     # press keycode
        #
        #     key=["home", "back", "left", "right", "up", "down", "center",
        #          "menu", "search", "enter", "delete", "del", "recent",
        #          "volume_up", "volume_down", "volume_mute", "camera", "power"]

    def press_home(self):
        return self.device.press.home()

    def press_back(self):
        return self.device.press.back()

    def press_menu(self):
        return self.device.press.menu()

    def press_recent(self):
        return self.device.press.recent()

    def press_keycode(self, keycode):
        return self.device.press(keycode)

if __name__ == '__main__':
    ui = UiAutomator('ce58ac0d')
    print ui.click(resourceId='com.android.contacts:id/user_profile_button')

