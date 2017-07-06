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

        return self.device.dump(filename=filename, compressed=compressed, pretty=pretty)

    def screenshot(self, filename, scale=1.0, quality=100):
        return self.device.screenshot(filename=filename, scale=scale, quality=quality)

    def click(self, **kwargs):
        Utility.output_msg('UIAUTOMATOR|CLICK|SELECTOR: %s' % str(kwargs))
        try:
            self.device(**kwargs).click()
            return True
        except JsonRPCError:
            return False

    def click_if_exists(self,text):
        if self.device(text=text).exists:
            self.device(text=text).click


    def long_click(self, **kwargs):
        try:
            return self.device(**kwargs).long_click()
        except JsonRPCError, e:
            return 'Error'

    def get_current_package_name(self):
        try:
            return self.device.info.get('currentPackageName')
        except Exception:
            return self.get_current_package_name()



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

    def edit(self, **kwargs):
        text = Utility.random_char(10)
        Utility.output_msg('Edit:%s' % kwargs)
        Utility.output_msg('Input:%s' % text)
        try:
            return self.device(**kwargs).set_text(text)
        except JsonRPCError, e:
            return 'Error'

    def exists(self, **kwargs):
        return self.device(**kwargs).exists

if __name__ == '__main__':
    ui = UiAutomator()
    #print ui.click(**{'className': u'android.widget.TextView', 'index': u'1', 'resourceId': u'com.android.contacts:id/menu_search', 'description': u'Search', 'text': u''})
    print ui.get_current_package_name()
