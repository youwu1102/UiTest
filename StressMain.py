# -*- encoding:UTF-8 -*-
from DebugMain import Debug
from libs.UiAutomator import UiAutomator
from libs.Utility import Utility
from libs.TraversalNode import TraversalNode
from libs.Dump import Analysis
from os.path import join
import os
import random
from xml.dom.minidom import parse
from libs.GlobalVariable import GlobalVariable
from libs.TimeFormat import TimeFormat

class Stress(Debug):
    def __init__(self, project, package_name, serial=None):
        Debug.__init__(self, project=project, package_name=package_name, serial=serial)
        self.root_log_folder = Utility.make_dirs(join(GlobalVariable.logs_directory, TimeFormat.timestamp(), package_name))
        self.test_count = 0

    def __parse_config(self):
        if os.path.exists(self.case_xml):
            dom = parse(self.case_xml)
            root = dom.documentElement
            nodes = root.getElementsByTagName('Node')
            for node in nodes:
                eigenvalue = node.getAttribute('eigenvalue')
                traversal_node = TraversalNode(eigenvalue=eigenvalue)
                next_list = node.getElementsByTagName('Next')
                previous_list = node.getElementsByTagName('Previous')
                closed_list = node.getElementsByTagName('All')
                optional_list = node.getElementsByTagName('Optional')
                for next_node in next_list:
                    for info_node in next_node.getElementsByTagName('Info'):
                        tmp_e = info_node.getAttribute('eigenvalue')
                        tmp_a = info_node.getAttribute('action')
                        traversal_node.append_next((tmp_e, eval(tmp_a)))
                for previous_node in previous_list:
                    for info_node in previous_node.getElementsByTagName('Info'):
                        tmp_e = info_node.getAttribute('eigenvalue')
                        tmp_a = info_node.getAttribute('action')
                        traversal_node.append_previous((tmp_e, eval(tmp_a)))
                for optional_node in optional_list:
                    for info_node in optional_node.getElementsByTagName('Info'):
                        tmp_a = info_node.getAttribute('action')
                        traversal_node.append_optional(eval(tmp_a))
                for closed_node in closed_list:
                    for info_node in closed_node.getElementsByTagName('Info'):
                        tmp_a = info_node.getAttribute('action')
                        traversal_node.append_closed(eval(tmp_a))
                self.dict_traversal_node[eigenvalue] = traversal_node
        else:
            Utility.output_msg('I can not find case config file')

    def main(self):
        self.__parse_config()
        while True:
            self.test_count += 1
            self.log_directory = Utility.make_dirs(join(self.root_log_folder, '%04d' % self.test_count))
            self.go_next_count = 0
            self.count = 0
            random_traversal_list = self.dict_traversal_node.keys()[:]
            if self.device.get_current_package_name() != self.package_name:
                Utility.start_process_on_device(self.package_name)

            self.go_to_target(target=random.choice(random_traversal_list))  #
            current_node = self.get_current_traversal_node()
            closed_list = current_node.get_closed()
            optional_list = current_node.get_optional()
            if closed_list:
                # for optional in optional_list:
                #     self.do_action(optional)
                self.do_action(random.choice(closed_list))
                self.set_current_dump_path()
                self.device.screenshot(self.current_dump_screenshot)

    def do_action(self, action):
        option = action.get('action')
        selector = self.get_selector(action=action)
        if option == 'Click':
            self.record_path(action='Click', selector=selector)
            return self.device.click(**selector)
        elif option == 'Edit':
            self.record_path(action='Edit', selector=selector)
            return self.device.edit(**selector)
        else:
            Utility.output_msg('Unknown option: %s.' % option)
            return False

    def record_path(self, action, selector):
        with open(join(self.log_directory, 'path.txt'), 'a') as w_file:
            w_file.write('%8s, %s\n' % (action, str(selector)))
        self.set_current_dump_path()
        self.device.screenshot(self.current_dump_screenshot)

    def get_current_traversal_node(self):  # 获取当前界面的节点
        tmp_path = join(self.root_log_folder, 'tmp.uix')
        self.device.dump(tmp_path)
        current_eigenvalue, current_window_nodes = Analysis.get_info_from_dump(tmp_path)
        if current_eigenvalue not in self.dict_traversal_node.keys():
            current_traversal_node = TraversalNode(current_eigenvalue)
            current_traversal_node.init_open(current_window_nodes)
            self.dict_traversal_node[current_eigenvalue] = current_traversal_node
            print 'I will append %s' % current_eigenvalue
            self.list_eigenvalue.append(current_eigenvalue)
            #os.rename(self.current_dump_screenshot,self.current_dump_screenshot.replace('.png', '.%s.png' % current_eigenvalue).replace('<','[').replace('>', ']'))
        else:
            current_traversal_node = self.dict_traversal_node.get(current_eigenvalue)
        return current_traversal_node

if __name__ == '__main__':
    package_name1 = "com.android.contacts"
    package_name1 = "com.android.mms"

    d = Stress(project='SDM660', package_name=package_name1)
    d.main()