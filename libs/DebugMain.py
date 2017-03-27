__author__ = 'c_youwu'
from UiAutomator import UiAutomator
from Utility import Utility
from GlobalVariable import GlobalVariable
from os.path import join

class Debug(object):
    def __init__(self, package_name, serial=None):
        self.package_name = package_name
        self.device = UiAutomator(serial)
        self.logs_directory = Utility.make_dirs(join(GlobalVariable.logs_directory, package_name))
        self.

    def main(self):
        print self.device.get_current_package_name()








if __name__ == '__main__':
    d = Debug(package_name='ss')
    d.main()