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

class Test(Debug):
    def __init__(self, project, package_name, serial=None):
        Debug.__init__(self, project=project, package_name=package_name, serial=serial)

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
                for next_node in next_list:
                    tmp_e = next_node.getAttribute('eigenvalue')
                    tmp_a = next_node.getAttribute('action')
                    traversal_node.append_next((tmp_e, eval(tmp_a)))
                for previous_node in previous_list:
                    tmp_e = previous_node.getAttribute('eigenvalue')
                    tmp_a = previous_node.getAttribute('action')
                    traversal_node.append_previous((tmp_e, eval(tmp_a)))
                self.dict_traversal_node[eigenvalue]=traversal_node
        else:
            Utility.output_msg('I can not find case config file')

    def main(self):
        self.__parse_config()
        list_eigenvalue = self.dict_traversal_node.keys()
        while True:
            self.go_next_count = 0
            if self.device.get_current_package_name() != self.package_name:
                Utility.start_process_on_device(self.package_name)
            self.go_to_target(target=random.choice(list_eigenvalue))  #





if __name__ == '__main__':
    package_name1 = "com.android.contacts"
    package_name1 = "com.android.mms"
    package_name1 = "com.android.deskclock"
    d = Test(project='SDM660', package_name=package_name1)
    d.main()