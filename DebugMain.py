# -*- encoding:UTF-8 -*-
from libs.UiAutomator import UiAutomator
from libs.Utility import Utility
from libs.GlobalVariable import GlobalVariable
from libs.TraversalNode import TraversalNode
from libs.Dump import Analysis
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
        self.previous_dump_node = None  # 上一个遍历节点
        self.previous_window_node = None  # 上一个遍历节点里的操作节点
        self.dict_traversal_node = dict()  # 每一个特征值对应一个遍历路径上的节点
        self.list_eigenvalue = list()  # 记录遍历节点出现的顺序
        self.__count = 0  # 计数器

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
            Utility.output_msg('=================================================================')
            eigenvalue = self.get_not_complete_node()
            if eigenvalue:# 判断是否全部结束了 没有再出现新节点
                self.enter_to_except_location(eigenvalue)  #
                self.tmp() #
            else:
                Utility.output_msg('All locations have been traversed.')
                break


    def dump_current_window(self):
        self.__set_current_dump_path()
        self.device.dump(self.current_dump)
        self.device.screenshot(self.current_dump_screenshot)


    def get_current_eigenvalue(self):
        self.device.dump('current')
        return Analysis.calculate_eigenvalue('current')

    def return_to_expect_location(self, except_location):  # 返回预期位置
        Utility.output_msg('I want to return to except window.')
        while self.get_current_eigenvalue() != except_location:
            Utility.output_msg('Current window is not the except window,press back key.')
            self.device.press_back()
            if self.device.get_current_package_name() != self.package_name:
                Utility.start_process_on_device(self.package_name)
                break

    def enter_to_except_location(self, expect_location):  # 进入预期位置
        current = self.get_current_eigenvalue()
        if current == expect_location:
            Utility.output_msg('Already in the except location.')
        else:
            self.calculated_path(current=current, target=expect_location)



    def calculated_path(self, current, target):
        pass

    def do_action(self, action):
        option = action.get('action')
        selector = self.get_selector(action=action)
        if option == 'Click':
            return self.device.click(**selector)
        else:
            Utility.output_msg('Unknown option: %s.' % option)
            return False

    def initialization(self):
        self.return_to_expect_location(except_location='')
        current_traversal_node = self.get_current_traversal_node()

    def tmp(self):
        before_action = self.get_current_traversal_node()   # 操作之前的 界面节点
        open_list = before_action.get_open()  # 获取操作之前的未执行过的操作
        if open_list:  # 如果不为空，就执行操作
            window_node = open_list[0]  # 获取第一个节点元素
            if self.do_action(action=window_node):  # 判断操作是否成功
                before_action.move_to_closed(window_node)  # 将操作步骤 从OPEN列表移动CLOSED列表
                after_action = self.get_current_traversal_node()  # 获取操作之后的界面节点
                if not self.is_current_window_legal(): #  判断当前节点是否合法 可能以后会在判断过程中把一些ALLOW的提醒点掉
                    Utility.output_msg('Current window is illegal.')
                    after_action.init_open([]) # 如果是非法的 则将这个节点里面的操作节点全部初始化为空
                    return
                if before_action is after_action:  # 判断节点是否为同一个
                    Utility.output_msg('Interface is not changed')
                else:
                    Utility.output_msg('Interface has changed')
                    after_action.append_previous({before_action.get_node_eigenvalue(): window_node})  # 操作的后的节点添加前继
                    before_action.append_next({after_action.get_node_eigenvalue(): window_node})  # 操作后的节点添加后继
            else:
                Utility.output_msg('Do Action Fail: %s' % str(window_node))
        else:  # 否则的话 就什么都不做了
            Utility.output_msg('%s' % before_action.get_node_eigenvalue())
            Utility.output_msg('All operations of current dump window have been completed')


    def get_current_traversal_node(self):  # 获取当前界面的节点
        self.dump_current_window()
        current_eigenvalue, current_window_nodes = Analysis.get_info_from_dump(self.current_dump)
        if current_eigenvalue not in self.dict_traversal_node:
            current_traversal_node = TraversalNode(current_eigenvalue)
            current_traversal_node.init_open(current_window_nodes)
            self.dict_traversal_node[current_eigenvalue] = current_traversal_node
            self.list_eigenvalue.append(current_eigenvalue)
        else:
            current_traversal_node = self.dict_traversal_node.get(current_eigenvalue)
        return current_traversal_node

    def __set_current_dump_path(self):  # 更新最新的dump路径，每次调用自动加1
        self.current_dump = join(self.log_directory, '%04d.uix' % self.__count)
        self.current_dump_screenshot = join(self.log_directory, '%04d.png' % self.__count)
        self.current_dump_txt = join(self.log_directory, '%04d.txt' % self.__count)
        self.__count += 1

    @classmethod
    def get_selector(cls, action):
        dict_tmp = dict()
        for key in GlobalVariable.dict_selector.keys():
            key_value = action.get(key)
            if key_value:
                dict_tmp[GlobalVariable.dict_selector.get(key)] = key_value
        return dict_tmp

    def get_not_complete_node(self):
        for eigenvalue in self.list_eigenvalue:
            traversal_node = self.dict_traversal_node.get(eigenvalue)
            open_list = traversal_node.get_open()
            if open_list:
                Utility.output_msg('Node: %s still has some nodes not be traversed' % traversal_node.get_node_eigenvalue())
                for i in open_list:
                    Utility.output_msg('\t%s' % str(i))
            return traversal_node
        return False

    def is_current_window_legal(self):
        if self.device.get_current_package_name() == self.package_name:
            return True
        return False

if __name__ == '__main__':
    package_name1 = "com.android.contacts"
    d = Debug(project='SDM660', package_name=package_name1)
    d.main()