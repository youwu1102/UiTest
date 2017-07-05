# -*- encoding:UTF-8 -*-
from libs.UiAutomator import UiAutomator
from libs.Utility import Utility
from libs.GlobalVariable import GlobalVariable
from libs.TraversalNode import TraversalNode
from libs.Dump import Analysis
from os.path import join
from xml.dom.minidom import Document
import os


class Debug(object):
    def __init__(self, project, package_name, serial=None, activity_name=''):
        self.project = project
        self.package_name = package_name
        self.activity_name = activity_name
        self.device = UiAutomator(serial)
        self.log_directory = Utility.make_dirs(join(GlobalVariable.logs_directory, package_name))
        self.case_directory = Utility.make_dirs(join(GlobalVariable.case_utils, project, package_name))
        self.case_xml = join(self.case_directory, 'Config.xml')
        self.current_dump = ''
        self.current_dump_txt = ''
        self.current_dump_screenshot = ''
        self.dict_traversal_node = dict()  # 每一个特征值对应一个遍历路径上的节点
        self.list_eigenvalue = list()  # 记录遍历节点出现的顺序
        self.list_retry_eigenvalue = list()
        self.count = 0  # 计数器
        self.go_next_count = 0
        self.return_count = 0

    def main(self):
        self.initialization()
        self.processing()
        self.finish()

    def initialization(self):
        # Utility.stop_process_on_device(self.package_name)
        # Utility.wait_for_time(2)
        # Utility.start_process_on_device(self.package_name, self.activity_name)
        # Utility.wait_for_time(10)
        current = self.get_current_traversal_node()
        current.set_level(0)

    def processing(self):
        while True:
            self.go_next_count = 0  # 这个参数放置一直重复循环在某一段无法抵达的情况
            self.return_count = 0  # 这个参数放置一直重复循环在某一段无法抵达的情况
            Utility.output_msg('======================while True Flag==========================')
            eigenvalue = self.get_not_complete_node()
            Utility.output_msg('%s node has not been fully traversed.' % eigenvalue)
            if eigenvalue:# 判断是否全部结束了 没有再出现新节点
                self.go_to_target(target=eigenvalue)  #
                self.tmp()# 执行步骤
            else:
                Utility.output_msg('All locations have been traversed.')
                break


    def set_current_dump_path(self):  # 更新最新的dump路径，每次调用自动加1
        self.current_dump = join(self.log_directory, '%04d.uix' % self.count)
        self.current_dump_screenshot = join(self.log_directory, '%04d.png' % self.count)
        self.current_dump_txt = join(self.log_directory, '%04d.txt' % self.count)
        self.count += 1

    def dump_current_window(self):
        self.set_current_dump_path()
        self.device.dump(self.current_dump)
        self.device.screenshot(self.current_dump_screenshot)

    def get_current_traversal_node(self):  # 获取当前界面的节点
        self.dump_current_window()
        current_eigenvalue, current_window_nodes = Analysis.get_info_from_dump(self.current_dump)
        if current_eigenvalue not in self.dict_traversal_node.keys():
            current_traversal_node = TraversalNode(current_eigenvalue)
            current_traversal_node.init_open(current_window_nodes)
            self.dict_traversal_node[current_eigenvalue] = current_traversal_node
            Utility.output_msg('I will append %s' % current_eigenvalue,level='i')
            self.list_eigenvalue.append(current_eigenvalue)
            #os.rename(self.current_dump_screenshot, self.current_dump_screenshot.replace('.png', '.%s.png' % current_eigenvalue).replace('<', '[').replace('>', ']'))
        else:
            current_traversal_node = self.dict_traversal_node.get(current_eigenvalue)
        return current_traversal_node

    def get_not_complete_node(self):
        for eigenvalue in self.list_eigenvalue:
            traversal_node = self.dict_traversal_node.get(eigenvalue)
            if not self.traversal_node_rule(traversal_node=traversal_node):
                continue
            open_list = traversal_node.get_open()
            if open_list:
                Utility.output_msg('Node: %s still has %s node(s) not be traversed' % (traversal_node.get_node_eigenvalue(), len(open_list)))
                for i in open_list:
                    Utility.output_msg('\t%s' % str(i), level='d')
                return traversal_node.get_node_eigenvalue()
        for eigenvalue in self.list_retry_eigenvalue:
            traversal_node = self.dict_traversal_node.get(eigenvalue)
            open_list = traversal_node.get_open()
            if open_list:
                Utility.output_msg('Node: %s still has %s node(s) not be traversed' % (traversal_node.get_node_eigenvalue(), len(open_list)))
                for i in open_list:
                    Utility.output_msg('\t%s' % str(i), level='d')
                return traversal_node.get_node_eigenvalue()
        return False

    def traversal_node_rule(self, traversal_node):
        open_list = traversal_node.get_open()
        if not open_list:  # 判断是否还有open的节点
            return False

        if traversal_node.get_level() > 5:  # 判断遍历层次是否大于10
            traversal_node.move_all_open_to_closed()
            return False

        for o in open_list:
            if o.get('package') != self.package_name:
                return False
            break
        return True



if __name__ == '__main__':
    package_name = "com.letv.android.client"
    activity_name = '.activity.MainActivity'
    d = Debug(project='SDM660', package_name=package_name,activity_name=activity_name)
    d.main()