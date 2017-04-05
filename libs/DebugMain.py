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
        self.current_dump = ''
        self.current_dump_txt = ''
        self.current_dump_screenshot = ''
        self.case_doc = Document()
        self.root_count = 0
        self.home = []

    def rename_case_xml(self):
        case_xml = join(self.case_directory, 'Config.xml')
        if os.path.exists(case_xml):
            Utility.output_msg('I find an old config file for %s, I will generate a new one.')
            for x in xrange(1, 10000):
                back_case_xml = join(self.case_directory, 'Config.xml.back%s' % x)
                if not os.path.exists(back_case_xml):
                    os.rename(case_xml, back_case_xml)
                    break
        return case_xml

    def main(self):
        self.initialization()
        self.return_home()
        #self.traversal_level_1(step='', count=self.root_count)

    def get_current_eigenvalue(self):
        self.device.dump('current')
        return Utility.calculate_eigenvalue('current')

    def return_home(self):
        Utility.output_msg('I want to return home page.')
        while self.get_current_eigenvalue() not in self.home:
            Utility.output_msg('is diff')
            self.device.press_back()
            if self.device.get_current_package_name() != self.package_name:
                Utility.start_process_on_device(self.package_name)
                self.home.append(self.get_current_eigenvalue())
                break

    def traversal_level_1(self, step, count):
        step = self.__set_current_dump_path(parent=step, count=count)
        self.device.dump(self.current_dump)
        self.device.screenshot(self.current_dump_screenshot)
        eigenvalue = Utility.analysis_dump(self.current_dump)
        if eigenvalue not in self.list_eigenvalue:
            self.list_eigenvalue.append(eigenvalue)
            self.dict_S_M_E[step] = eigenvalue
            actions = GlobalVariable.dict_E_M_A.get(eigenvalue)
            with open(self.current_dump_txt, 'w') as w_file:
                for x in range(len(actions)):
                    w_file.write(str(actions[x])+'\r')

        else:
            print 'sss'




        # root = self.traversal_path('Root')
        # self.case_doc.appendChild(root)
        # f = open(self.case_xml, "w")
        # f.write(self.case_doc.toprettyxml(indent='\t', encoding='utf-8'))
        # f.close()
        # while True:
        #     count += 1
        #     self.__set_current_dump_path(dump_name=count)
        #
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

    # def traversal_path(self, parent):
    #     self.__set_current_dump_path()
    #
    #     # if parent == 'Root':
    #     #     Utility.output_msg('Create \"ROOT\" node.')
    #     #     parent = self.case_doc.createElement("Root")
    #     # self.device.dump(self.current_dump)
    #     # self.device.screenshot(self.current_dump_screenshot)
    #     # eigenvalue = Utility.analysis_dump(self.current_dump)
    #     # actions = GlobalVariable.dict_E_M_A.get(eigenvalue)
    #     # tmp = actions[:]
    #     # for action in tmp:
    #     #     node = self.case_doc.createElement('Node')
    #     #     node.setAttribute('eigenvalue', eigenvalue)
    #     #     for key in action.keys():
    #     #         node.setAttribute(key, action.get(key))
    #     #     self.do_action(action)
    #     #     actions.remove(action)
    #     #     self.traversal_path(node)
    #     #     parent.appendChild(node)
    #     # self.device.press_back()
    #
    #     return parent
    #



    def do_action(self, action):
        option = action.get('action')
        selector = Utility.get_selector(action=action)
        if option == 'Click':
            return self.device.click(**selector)
        else:
            Utility.output_msg('Unknown option: %s.' % option)

    def __set_current_dump_path(self, name):
        self.current_dump = join(self.log_directory, '%s.uix' % name)
        self.current_dump_screenshot = join(self.log_directory, '%s.png' % name)
        self.current_dump_txt = join(self.log_directory, '%s.txt' % name)
        return name

    def initialization(self):
        self.__set_current_dump_path(name=0)
        self.device.dump(self.current_dump)
        self.device.screenshot(self.current_dump_screenshot)
        self.home.append(Utility.calculate_eigenvalue(self.current_dump))



if __name__ == '__main__':

    package_name1 = "com.android.contacts"
    d = Debug(project='SDM660', package_name=package_name1)
    d.main()