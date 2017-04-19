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
        self.dict_traversal_node = dict()  # 每一个特征值对应一个遍历路径上的节点
        self.list_eigenvalue = list()  # 记录遍历节点出现的顺序
        self.list_retry_eigenvalue = list()
        self.__count = 0  # 计数器
        self.__go_next_count = 0

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
            self.__go_next_count = 0  # 这个参数放置一直重复循环在某一段无法抵达的情况
            Utility.output_msg('======================while True Flag==========================')
            eigenvalue = self.get_not_complete_node()
            Utility.output_msg('%s node has not been fully traversed.' % eigenvalue)
            if eigenvalue:# 判断是否全部结束了 没有再出现新节点
                self.go_to_target(target=eigenvalue)  #
                self.tmp()# 执行步骤
            else:
                Utility.output_msg('All locations have been traversed.')
                break

    def write_node_config(self):
        pass

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
                if self.get_current_eigenvalue() == except_location:
                    return True
                return False
        Utility.output_msg('Function return_to_expect_location over.', 'd')
        return True

    def enter_to_except_location(self, expect_location):  # 进入预期位置
        current = self.get_current_eigenvalue()
        if current == expect_location:
            Utility.output_msg('Already in the except location.')
            return True
        else:
            return self.calculated_path(current=current, target=expect_location)

    def calculated_path(self, current, target):
        dict_previous = dict()
        dict_next = dict()

        self.__find_in_next(target=target, dict_path=dict_next)
        print dict_next
        if current in dict_next:
            print 'next'
            return self.__go_next(dict_next=dict_next,target=target)

        self.__find_in_previous(current=current, dict_path=dict_previous)
        print dict_previous
        if target in dict_previous:
            print 'previous'
            return self.return_to_expect_location(target)

        brother_result = self.__find_in_brother(current=current, target=target, dict_previous=dict_previous, dict_next=dict_next)
        if brother_result:
            print 'brother'
            Utility.output_msg('I will return to ##%s## first.' % brother_result)
            self.return_to_expect_location(except_location=brother_result)
            return self.__go_next(dict_next=dict_next,target=target)
        self.__exceptional_handling(eigenvalue=target)
        return False

    def __exceptional_handling(self, eigenvalue):
        if eigenvalue in self.list_eigenvalue:
            self.list_eigenvalue.remove(eigenvalue)
            self.list_retry_eigenvalue.append(eigenvalue)
        elif eigenvalue in self.list_retry_eigenvalue:
            self.list_retry_eigenvalue.remove(eigenvalue)
        else:
            Utility.output_msg('Fun:__exceptional_handling', 'e')

    def __go_next(self, dict_next, target):
        if self.__go_next_count > 20:
            self.__exceptional_handling(eigenvalue=target)
            return True
        self.__go_next_count += 1
        current = self.get_current_eigenvalue()
        if current != target:
            if dict_next.get(current) is None:
                Utility.output_msg('I can not get next step')
                return False
            self.do_action(dict_next.get(current))
            self.__go_next(dict_next=dict_next, target=target)
        else:
            return True

    def __find_in_previous(self, current, dict_path):
        current_node = self.dict_traversal_node.get(current)
        while current_node is None:
            self.device.press_back()
            current_node = self.get_current_traversal_node()

        for e, a in current_node.get_previous():
            if e in dict_path.keys():  # 如果PATH LIST已经包含了这个路径  那么认为这是一条重复路径则不进行下去了
                continue
            else:
                dict_path[e] = a
                self.__find_in_previous(current=e, dict_path=dict_path)


    def __find_in_next(self, target, dict_path):
        target_node = self.dict_traversal_node.get(target)
        for e, a in target_node.get_previous():
            if e in dict_path.keys():  # 如果PATH LIST已经包含了这个路径  那么认为这是一条重复路径则不进行下去了
                continue
            else:
                dict_path[e] = a
                self.__find_in_next(target=e, dict_path=dict_path)

    def __find_in_brother(self, current, target, dict_previous,dict_next):
        for key in dict_previous.keys():
            if key in dict_next.keys():
                return key
        return False

    def go_to_target(self, target):
        Utility.output_msg('I want go to the target: %s' % target)
        current = self.get_current_eigenvalue()
        if current == target:
            Utility.output_msg('Already in the target: %s' % target)
            return True
        self.calculated_path(current=current, target=target)

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
        self.get_current_traversal_node()

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
                    after_action.append_previous((before_action.get_node_eigenvalue(), window_node))  # 操作的后的节点添加前继
                    before_action.append_next((after_action.get_node_eigenvalue(), window_node))  # 操作后的节点添加后继
                    return
                if before_action is after_action:  # 判断节点是否为同一个
                    Utility.output_msg('Interface is not changed')
                else:
                    Utility.output_msg('Interface has changed')
                    after_action.append_previous((before_action.get_node_eigenvalue(), window_node))  # 操作的后的节点添加前继
                    before_action.append_next((after_action.get_node_eigenvalue(), window_node))  # 操作后的节点添加后继
            else:
                Utility.output_msg('Do Action Fail: %s' % str(window_node))
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
                    after_action.append_previous((before_action.get_node_eigenvalue(), window_node))  # 操作的后的节点添加前继
                    before_action.append_next((after_action.get_node_eigenvalue(), window_node))  # 操作后的节点添加后继
        else:  # 否则的话 就什么都不做了
            Utility.output_msg('%s' % before_action.get_node_eigenvalue())
            Utility.output_msg('All operations of current dump window have been completed')


    def get_current_traversal_node(self):  # 获取当前界面的节点
        self.dump_current_window()
        current_eigenvalue, current_window_nodes = Analysis.get_info_from_dump(self.current_dump)
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

    def is_current_window_legal(self):
        if self.device.get_current_package_name() == self.package_name:
            return True
        return False

if __name__ == '__main__':
    package_name1 = "com.android.contacts"
    package_name1 = "com.android.mms"
    d = Debug(project='SDM660', package_name=package_name1)
    d.main()