# -*- encoding:UTF-8 -*-
from libs.UiAutomator import UiAutomator
from libs.Utility import Utility
from libs.GlobalVariable import GlobalVariable
from libs.TraversalNode import TraversalNode
from libs.Dump import Analysis
from os.path import join
from xml.dom.minidom import Document
import os
from time import sleep


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
        # Utility.start_process_on_device(self.package_name, self.activity_name)
        current = self.get_current_traversal_node()
        current.set_level(0)

    def processing(self):
        while True:
            self.go_next_count = 0  # 这个参数放置一直重复循环在某一段无法抵达的情况
            self.return_count = 0  # 这个参数放置一直重复循环在某一段无法抵达的情况
            Utility.output_msg('PROCESSING|WHILE:START')
            eigenvalue = self.get_not_complete_node()
            if eigenvalue:# 判断是否全部结束了 没有再出现新节点
                Utility.output_msg('PROCESSING|NODE:%s' % eigenvalue)
                if self.go_to_target(target=eigenvalue):   # 如果找到节点位置  则重置尝试次数
                    self.dict_traversal_node.get(eigenvalue).reset_attempts()
                else:  # 否则增加次数
                    self.dict_traversal_node.get(eigenvalue).add_attempts()
                self.action()   #无论是否找到  都会执行一步操作
            else:
                Utility.output_msg('All locations have been traversed.')
                break
            Utility.output_msg('PROCESSING|WHILE:END')

    def go_to_target(self, target):
        current = self.get_current_eigenvalue()
        Utility.output_msg('GO_TO_TARGET|C:%s' % current)
        Utility.output_msg('GO_TO_TARGET|T:%s' % target)
        if current == target:
            Utility.output_msg('GO_TO_TARGET|DONE')
            return True
        # 上面描述了 如果过当前节点是目标节点 则返回TRUE
        # 下面描述了 经过计算后，再一次获取当前节点，是否符合需求，然后根据实际情况返回True or False
        else:
            self.calculated_path(current=current, target=target)
            current = self.get_current_eigenvalue()
            if current == target:
                Utility.output_msg('GO_TO_TARGET|DONE')
                return True
            else:
                Utility.output_msg('GO_TO_TARGET|FAIL')
                return False


    def get_current_eigenvalue(self):
        self.device.dump('current')
        return Analysis.calculate_eigenvalue('current')

    def calculated_path(self, current, target):
        dict_previous = dict()
        dict_next = dict()
        self.find_in_next(target=target, dict_path=dict_next)
        if current in dict_next:
            print 'next'
            return self.go_next(dict_next=dict_next,target=target)
        self.find_in_previous(current=current, dict_path=dict_previous)
        if target in dict_previous:
            print 'previous'
            return self.return_to_expect_location(target)

        brother_result = self.find_in_brother(dict_previous=dict_previous, dict_next=dict_next)
        if brother_result:
            print 'brother'
            Utility.output_msg('I will return to ##%s## first.' % brother_result)
            self.return_to_expect_location(except_location=brother_result)
            return self.go_next(dict_next=dict_next,target=target)
        self.exceptional_handling(eigenvalue=target)
        return False

    def find_in_next(self, target, dict_path):
        target_node = self.dict_traversal_node.get(target)
        for e, a in target_node.get_previous():
            if e in dict_path.keys():  # 如果PATH LIST已经包含了这个路径  那么认为这是一条重复路径则不进行下去了
                continue
            else:
                dict_path[e] = a
                self.find_in_next(target=e, dict_path=dict_path)

    def action(self):
        # 会先获取一次操作前的界面
        # 然后判断里面是否有空的节点
        # 如果全部已经完成 则完成
        #
        Utility.output_msg('ACTION|START')
        before_action = self.get_current_traversal_node()   # 操作之前的 界面节点
        open_list = before_action.get_open()  # 获取操作之前的未执行过的操作
        Utility.output_msg('ACTION|BEFORE|NODE|EIGI:%s' % before_action.get_node_eigenvalue())
        Utility.output_msg('ACTION|BEFORE|NODE|OPEN:%s' % len(before_action.get_open()))
        if open_list:  # 如果不为空，就执行操作
            window_node = open_list[0]  # 获取第一个节点元素
            if not self.do(action=window_node):
                Utility.output_msg('ACTION|UIAUTOMATION|EXCEPTION')
                return
            after_action = self.get_current_traversal_node()  # 获取操作之后的界面节点
            Utility.output_msg('ACTION|AFTER|NODE|EIGI:%s' % after_action.get_node_eigenvalue())
            Utility.output_msg('ACTION|AFTER|NODE|OPEN:%s' % len(after_action.get_open()))

            if not self.is_current_window_legal(): #  判断当前节点是否合法
                Utility.output_msg('ACTION|AFTER|ILLEGAL')
                before_action.move_to_closed(window_node)  # 将操作步骤 从OPEN列表移动CLOSED列表
                after_action.move_all_open_to_optional()  # 如果是非法的 则将这个节点里面的操作节点全部修改到closed状态
                after_action.append_previous((before_action.get_node_eigenvalue(), window_node))  # 操作的后的节点添加前继
                before_action.append_next((after_action.get_node_eigenvalue(), window_node))  # 操作后的节点添加后继
                return
            if before_action is after_action:  # 判断节点是否为同一个
                Utility.output_msg('ACTION|AFTER|SAME')
                before_action.move_to_optional(window_node)
            else:
                Utility.output_msg('ACTION|AFTER|NORMAL')
                before_action.move_to_closed(window_node)  # 将操作步骤 从OPEN列表移动CLOSED列表
                after_action.set_level(before_action.get_level()+1)
                after_action.append_previous((before_action.get_node_eigenvalue(), window_node))  # 操作的后的节点添加前继
                before_action.append_next((after_action.get_node_eigenvalue(), window_node))  # 操作后的节点添加后继
        Utility.output_msg('ACTION|END')


    def set_current_dump_path(self):  # 更新最新的dump路径，每次调用自动加1
        self.current_dump = join(self.log_directory, '%04d.uix' % self.count)
        self.current_dump_screenshot = join(self.log_directory, '%04d.png' % self.count)
        self.current_dump_txt = join(self.log_directory, '%04d.txt' % self.count)
        self.count += 1

    def dump_current_window(self):
        self.set_current_dump_path()
        Utility.output_msg('DUMP_WINDOW|U:%s' % self.current_dump)
        self.device.dump(self.current_dump)
        Utility.output_msg('DUMP_WINDOW|S:%s' % self.current_dump_screenshot)
        self.device.screenshot(self.current_dump_screenshot)

    def get_current_traversal_node(self):  # 获取当前界面的节点
        self.dump_current_window()
        current_eigenvalue, current_window_nodes = Analysis.get_info_from_dump(self.current_dump)
        if current_eigenvalue not in self.dict_traversal_node.keys():
            Utility.output_msg('SYSTEM|NEW:%s' % current_eigenvalue)
            current_traversal_node = TraversalNode(current_eigenvalue)
            current_traversal_node.init_open(current_window_nodes)
            self.dict_traversal_node[current_eigenvalue] = current_traversal_node
            self.list_eigenvalue.append(current_eigenvalue)
            #os.rename(self.current_dump_screenshot, self.current_dump_screenshot.replace('.png', '.%s.png' % current_eigenvalue).replace('<', '[').replace('>', ']'))
        else:
            Utility.output_msg('SYSTEM|GET:%s' % current_eigenvalue)
            current_traversal_node = self.dict_traversal_node.get(current_eigenvalue)
        return current_traversal_node

    def get_not_complete_node(self):
        for eigenvalue in self.list_eigenvalue:
            traversal_node = self.dict_traversal_node.get(eigenvalue)
            if not self.traversal_node_rule(traversal_node=traversal_node):
                continue
            open_list = traversal_node.get_open()
            if open_list:
                Utility.output_msg('NOT_COMPLETE|NODE|EIGE:%s' % traversal_node.get_node_eigenvalue())
                Utility.output_msg('NOT_COMPLETE|NODE|OPEN:%s' % len(open_list))
                # for o in open_list:
                #     Utility.output_msg('NOT_COMPLETE|NODE| ACT:%s' % str(o))
                return traversal_node.get_node_eigenvalue()
        return None
        # for eigenvalue in self.list_retry_eigenvalue:
        #     traversal_node = self.dict_traversal_node.get(eigenvalue)
        #     open_list = traversal_node.get_open()
        #     if open_list:
        #         Utility.output_msg('Node: %s still has %s node(s) not be traversed' % (traversal_node.get_node_eigenvalue(), len(open_list)))
        #         for i in open_list:
        #             Utility.output_msg('\t%s' % str(i), level='d')
        #         return traversal_node.get_node_eigenvalue()
        # return False

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

    def do(self, action):
        option = action.get('action')
        selector = self.get_selector(action=action)
        if option == 'Click':
            return self.device.click(**selector)
            Utility.output_msg('Unknown option: %s.' % option)
            return False

    @classmethod
    def get_selector(cls, action):
            # dict_selector = {'text': 'text',
            #          'resource-id': 'resourceId',
            #          'content-desc': 'description',
            #          'class': 'className'}
        dict_tmp = dict()
        text = action.get('text')
        if text:
            dict_tmp['text'] = text
            return dict_tmp
        desc = action.get('content-desc')
        if desc:
            dict_tmp['description'] = desc
            return dict_tmp
        for key in GlobalVariable.dict_selector.keys():
            key_value = action.get(key)
            if key_value:
                dict_tmp[GlobalVariable.dict_selector.get(key)] = key_value
        return dict_tmp

    def is_current_window_legal(self):
        current_package_name = self.device.get_current_package_name()
        if current_package_name == self.package_name:
            return True
        elif current_package_name is None:
            self.device.press_recent()
            sleep(1)
            self.device.press_back()
            sleep(1)
            return self.is_current_window_legal()
        else:
            self.device.dump(join(self.log_directory, 'illegal%04d.uix' % self.count))
            self.device.screenshot(join(self.log_directory, 'illegal%04d.png' % self.count))
            for text in GlobalVariable.watch_list:
                self.device.click_if_exists(text=text)
            return self.device.get_current_package_name() == self.package_name

if __name__ == '__main__':
    package_name = "com.letv.android.client"
    activity_name = '.activity.MainActivity'
    d = Debug(project='SDM660', package_name=package_name,activity_name=activity_name)
    d.main()