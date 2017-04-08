__author__ = 'c_youwu'
from UiAutomator import UiAutomator
from Utility import Utility
from GlobalVariable import GlobalVariable
from TraversalNode import TraversalNode
from os.path import join
import os



class Debug(object):
    def __init__(self, project, package_name, serial=None):
        self.project = project
        self.package_name = package_name
        self.device = UiAutomator(serial)
        self.log_directory = Utility.make_dirs(join(GlobalVariable.logs_directory, package_name))
        self.case_directory = Utility.make_dirs(join(GlobalVariable.case_utils, project, package_name))
        self.case_xml = self.rename_case_xml()
        self.current_dump = ''
        self.current_dump_txt = ''
        self.current_dump_screenshot = ''
        self.list_home = []
        self.count = 0

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
        while True:

            ce = Utility.analysis_dump(self.current_dump) # ce = current eigenvalue
            cn = GlobalVariable.dict_E_M_N.get(ce) # cn = current node
            if cn.get_open():
                self.do_action(cn)
            else:
                self.device.press_back()

    def dump_current_window(self):
        self.__set_current_dump_path(name='%04d' % self.count)
        self.device.dump(self.current_dump)
        self.device.screenshot(self.current_dump_screenshot)


    def get_current_eigenvalue(self):
        self.device.dump('current')
        return Utility.calculate_eigenvalue('current')

    def return_home(self):
        Utility.output_msg('I want to return home window.')
        while self.get_current_eigenvalue() not in self.list_home:
            Utility.output_msg('Current windos is not home window,press back key.')
            self.device.press_back()
            if self.device.get_current_package_name() != self.package_name:
                Utility.start_process_on_device(self.package_name)
                self.list_home.append(self.get_current_eigenvalue())
                break

    def get_dump_text_file_path(self, name):
        return join(self.log_directory, '%s.txt' % name)


    def traversal_level_1(self, root):
        with open(self.get_dump_text_file_path(name=root)) as r:
            content = r.readlines()
            print content
        eigenvalue = content[0].strip('\r\n')
        actions = GlobalVariable.dict_E_M_A.get(eigenvalue)
        for x in range(len(actions)):
            self.do_action(actions[x])
            self.generate_dump_file('%s|%s' % (root, x))
            self.device.press_back()
            if self.get_current_eigenvalue() != eigenvalue:
                print 'sssssssssssssssssssssss'
                self.return_home()



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



    def do_action(self, current_node):
        action = current_node.get_open()[0]
        option = action.get('action')
        selector = Utility.get_selector(action=action)
        if option == 'Click':
            if self.device.click(**selector):
                current_node.move_to_closed(action)

        else:
            Utility.output_msg('Unknown option: %s.' % option)

    def __set_current_dump_path(self):
        self.current_dump = join(self.log_directory, '%04d.uix' % self.count)
        self.current_dump_screenshot = join(self.log_directory, '%04d.png' % self.count)
        self.current_dump_txt = join(self.log_directory, '%04d.txt' % self.count)
        self.count += 1

    def initialization(self):
        self.return_home()



    def generate_dump_file(self,name):
        self.__set_current_dump_path(name=name)
        self.device.dump(self.current_dump)
        self.device.screenshot(self.current_dump_screenshot)
        eigenvalue = Utility.analysis_dump(self.current_dump)
        return eigenvalue

    def tmp(self):
        self.__set_current_dump_path()
        current_eigenvalue = Utility.analysis_dump(self.current_dump)
        current_nodes = GlobalVariable.dict_E_M_N.get(current_eigenvalue)




if __name__ == '__main__':

    package_name1 = "com.android.contacts"
    d = Debug(project='SDM660', package_name=package_name1)
    d.main()