__author__ = 'c_youwu'
from UiAutomator import UiAutomator
from Utility import Utility
from GlobalVariable import GlobalVariable
from os.path import join



class Debug(object):
    def __init__(self, project, package_name, serial=None):
        self.project = project
        self.package_name = package_name
        self.device = UiAutomator(serial)
        self.log_directory = Utility.make_dirs(join(GlobalVariable.logs_directory, Utility.get_timestamp(), package_name))
        self.case_directory = Utility.make_dirs(join(GlobalVariable.case_utils, project, package_name))
        self.current_dump = ''
        self.current_dump_screenshot = ''

    def main(self):
        self.initialization()
        count = 0
        while True:
            count += 1
            self.__set_current_dump_path(dump_name=count)
            self.device.dump(self.current_dump)
            self.device.screenshot(self.current_dump_screenshot)
            eigenvalue = Utility.analysis_dump(self.current_dump)
            actions = GlobalVariable.dict_dump_actions.get(eigenvalue)
            if len(actions) > 0:
                print actions
                GlobalVariable.dict_dump_actions[eigenvalue] = []
            else:
                self.device.press_back()



    def __set_current_dump_path(self, dump_name):
        self.current_dump = join(self.log_directory, '%s.uix' % dump_name)
        self.current_dump_screenshot = join(self.log_directory, '%s.png' % dump_name)

    def initialization(self):
        Utility.restart_process_on_devices(self.package_name)


if __name__ == '__main__':
    package_name = "com.android.contacts"
    d = Debug(project='SDM660', package_name=package_name)
    d.main()