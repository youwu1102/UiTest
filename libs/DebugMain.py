__author__ = 'c_youwu'
from UiAutomator import UiAutomator
from Utility import Utility
from GlobalVariable import GlobalVariable
from os.path import join
import os
from xml.dom.minidom import Document


class Debug(object):
    def __init__(self, project, package_name, serial=None):
        self.project = project
        self.package_name = package_name
        self.device = UiAutomator(serial)
        self.log_directory = Utility.make_dirs(join(GlobalVariable.logs_directory, Utility.get_timestamp(), package_name))
        self.case_directory = Utility.make_dirs(join(GlobalVariable.case_utils, project, package_name))
        self.case_xml = self.rename_case_xml()
        self.traversal_times = 0
        self.current_dump = ''
        self.current_dump_screenshot = ''
        self.case_doc = Document()

    def rename_case_xml(self):
        case_xml = join(self.case_directory, 'Config.xml')
        if os.path.exists(case_xml):
            for x in xrange(1, 10000):
                back_case_xml = join(self.case_directory, 'Config.xml.back%s' % x)
                if not os.path.exists(back_case_xml):
                    os.rename(case_xml, back_case_xml)
                    break
        return case_xml


    def main(self):
        self.initialization()
        root = self.traversal_path('Root')
        self.case_doc.appendChild(root)
        f = open(self.case_xml, "w")
        f.write(self.case_doc.toprettyxml(indent='\t', encoding='utf-8'))
        f.close()
        # while True:
        #     count += 1
        #     self.__set_current_dump_path(dump_name=count)
        #     self.device.dump(self.current_dump)
        #     self.device.screenshot(self.current_dump_screenshot)
        #     eigenvalue = Utility.analysis_dump(self.current_dump)
        #     self.traversal_path('Root',)

            # actions = GlobalVariable.dict_dump_actions.get(eigenvalue)
            # if len(actions) > 0:
            #     print actions
            #     GlobalVariable.dict_dump_actions[eigenvalue] = []
            # else:
            #     self.device.press_back()

    def __create_xml(self):
        pass

    def traversal_path(self, parent):
        self.__set_current_dump_path()
        if parent == 'Root':
            parent = self.case_doc.createElement("Root")
        self.device.dump(self.current_dump)
        self.device.screenshot(self.current_dump_screenshot)
        eigenvalue = Utility.analysis_dump(self.current_dump)
        actions = GlobalVariable.dict_dump_actions.get(eigenvalue)
        for action in actions:
            node = self.case_doc.createElement('Node')
            for key in action.keys():
                node.setAttribute(key, action.get(key))
            print action
            parent.appendChild(node)
        self.device.press_back()
        return parent


    def do_action(self,action):
        act = action.get('action')
        if act == 'Click':
            self.device.click()



    @staticmethod
    def get_selector(action):
        dict_tmp = dict()


      return








    def __set_current_dump_path(self):
        self.traversal_times += 1
        self.current_dump = join(self.log_directory, '%s.uix' % self.traversal_times)
        self.current_dump_screenshot = join(self.log_directory, '%s.png' % self.traversal_times)

    def initialization(self):
        Utility.restart_process_on_devices(self.package_name)


if __name__ == '__main__':

    package_name1 = "com.android.contacts"
    d = Debug(project='SDM660', package_name=package_name1)
    d.main()