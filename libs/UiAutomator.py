# -*- encoding:UTF-8 -*-
from uiautomator import Device
from uiautomator import JsonRPCError
from Utility import Utility


# http://xiaocong.github.io/slides/android-uiautomator-and-python/#/first-usage
class UiAutomator(object):
    def __init__(self, serial=None):
        self.device = Device(serial)

    def info(self):
        return self.device.info

    def dump(self, filename=None, compressed=True, pretty=True):
        Utility.output_msg('Dump device window and pull to \"%s\".' % filename)
        return self.device.dump(filename=filename, compressed=compressed, pretty=pretty)

    def screenshot(self, filename, scale=1.0, quality=100):
        Utility.output_msg('Take screenshot and save to \"%s\".' % filename)
        return self.device.screenshot(filename=filename, scale=scale, quality=quality)

    def click(self, **kwargs):
        Utility.output_msg('Click:%s' % kwargs)
        try:
            return self.device(**kwargs).click()
        except JsonRPCError, e:
            Utility.output_msg(e, 'e')
            return False

    def long_click(self, **kwargs):
        try:
            return self.device(**kwargs).long_click()
        except JsonRPCError, e:
            Utility.output_msg(e, 'e')
            return False

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
        Utility.output_msg('Press Home Key')
        return self.device.press.home()

    def press_back(self):
        Utility.output_msg('Press Back Key')
        return self.device.press.back()

    def press_menu(self):
        Utility.output_msg('Press Menu Key')
        return self.device.press.menu()

    def press_recent(self):
        Utility.output_msg('Press Recent Key')
        return self.device.press.recent()

    def press_keycode(self, keycode):
        Utility.output_msg('Input Key Code: %s' % keycode)
        return self.device.press(keycode)

if __name__ == '__main__':
    ui = UiAutomator()
    print ui.click(**{'className': u'android.widget.TextView', 'index': u'1', 'resourceId': u'com.android.contacts:id/menu_search', 'description': u'Search', 'text': u''})

