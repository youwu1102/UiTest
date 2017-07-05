# -*- encoding:UTF-8 -*-
from libs.UiAutomator import UiAutomator
from libs.Utility import Utility
from libs.GlobalVariable import GlobalVariable
from libs.TraversalNode import TraversalNode
from libs.Dump import Analysis
from os.path import join
import os
from xml.dom.minidom import Document
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

    def rename_case_xml(self):
        if os.path.exists(self.case_xml):
            Utility.output_msg('I find an old config file for %s, I will generate a new one.')
            for x in xrange(1, 10000):
                back_case_xml = join(self.case_directory, 'Config.xml.back%s' % x)
                if not os.path.exists(back_case_xml):
                    os.rename(self.case_xml, back_case_xml)
                    break
        return self.case_xml

    def main(self):
        self.initialization()
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
        self.write_node_config()

    def __establish_node1(self, nodes, element_name, doc):
        xml_node = doc.createElement(element_name)
        for _node in nodes:
            print str(_node)
            _tmp = doc.createElement('Info')
            _tmp.setAttribute('action', str(_node))
            xml_node.appendChild(_tmp)
        return xml_node

    def __establish_node2(self, nodes, element_name, doc):
        xml_node = doc.createElement(element_name)
        for _node in nodes:
            print str(_node)
            _tmp = doc.createElement('Info')
            _tmp.setAttribute('eigenvalue', _node[0])
            _tmp.setAttribute('action', str(_node[1]))
            xml_node.appendChild(_tmp)
        return xml_node


    def write_node_config(self):
        config_xml = self.rename_case_xml()
        doc = Document()
        root = doc.createElement('Root')
        for value in self.dict_traversal_node.values():
            #value = self.dict_traversal_node.get(ei)
            node = doc.createElement('Node')
            node.setAttribute('eigenvalue', value.get_node_eigenvalue())
            node.setAttribute('level', str(value.get_level()))
            next_list = value.get_next()
            previous_list = value.get_previous()
            closed_list = value.get_closed()
            optional_list = value.get_optional()
            if next_list:
                node.appendChild(self.__establish_node2(nodes=next_list,element_name='Next', doc=doc))
            if previous_list:
                node.appendChild(self.__establish_node2(nodes=previous_list,element_name='Previous', doc=doc))
            if closed_list:
                node.appendChild(self.__establish_node1(nodes=closed_list,element_name='All', doc=doc))
            if optional_list:
                node.appendChild(self.__establish_node1(nodes=optional_list,element_name='Optional', doc=doc))
            root.appendChild(node)
        doc.appendChild(root)
        f = open(config_xml, 'w')
        f.write(doc.toprettyxml(indent='', encoding='utf-8'))
        f.close()

    def dump_current_window(self):
        self.set_current_dump_path()
        self.device.dump(self.current_dump)
        self.device.screenshot(self.current_dump_screenshot)

    def get_current_eigenvalue(self):
        self.device.dump('current')
        return Analysis.calculate_eigenvalue('current')

    def return_to_expect_location(self, except_location):  # 返回预期位置
        Utility.output_msg('I want to return to except window.')
        while self.get_current_eigenvalue() != except_location:
            self.return_count += 1
            Utility.output_msg('Current window is not the except window,press back key.')
            self.device.press_back()
            if self.device.get_current_package_name() != self.package_name:
                for x in range(10):
                    current_package_name = self.device.get_current_package_name()
                    if current_package_name == self.package_name:
                        break
                    elif current_package_name is None:
                        self.device.press_recent()
                        sleep(1)
                        self.device.press_back()
                        sleep(1)
                    else:
                        Utility.start_process_on_device(package=self.package_name, activity=self.activity_name)
                        sleep(2)
                if self.get_current_eigenvalue() == except_location:
                    return True
                return False
            if self.device.exists(text='OK'):
                self.device.click(text='OK')
            if self.return_count > 10:
                self.exceptional_handling(eigenvalue=except_location)
                return False
            sleep(0.5)
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

    def exceptional_handling(self, eigenvalue):
        self.device.press_back()
        if eigenvalue in self.list_eigenvalue:
            self.list_eigenvalue.remove(eigenvalue)
            self.list_retry_eigenvalue.append(eigenvalue)
        elif eigenvalue in self.list_retry_eigenvalue:
            self.list_retry_eigenvalue.remove(eigenvalue)
        else:
            Utility.output_msg('Fun:__exceptional_handling', 'e')

    def go_next(self, dict_next, target):
        if self.go_next_count > 20:
            self.exceptional_handling(eigenvalue=target)
            return True
        self.go_next_count += 1
        current = self.get_current_eigenvalue()
        if current != target:
            if dict_next.get(current) is None:
                Utility.output_msg('I can not get next step')
                return False
            self.do_action(dict_next.get(current))
            self.go_next(dict_next=dict_next, target=target)
        else:
            return True

    def find_in_previous(self, current, dict_path):
        current_node = self.dict_traversal_node.get(current)
        while current_node is None:
            self.device.press_back()
            current_node = self.get_current_traversal_node()

        for e, a in current_node.get_previous():
            if e in dict_path.keys():  # 如果PATH LIST已经包含了这个路径  那么认为这是一条重复路径则不进行下去了
                continue
            else:
                dict_path[e] = a
                self.find_in_previous(current=e, dict_path=dict_path)


    def find_in_next(self, target, dict_path):
        target_node = self.dict_traversal_node.get(target)
        for e, a in target_node.get_previous():
            if e in dict_path.keys():  # 如果PATH LIST已经包含了这个路径  那么认为这是一条重复路径则不进行下去了
                continue
            else:
                dict_path[e] = a
                self.find_in_next(target=e, dict_path=dict_path)

    def find_in_brother(self, dict_previous,dict_next):
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
        elif option == 'Edit':
            return self.device.edit(**selector)
        else:
            Utility.output_msg('Unknown option: %s.' % option)
            return False

    def initialization(self):
        self.return_to_expect_location(except_location='')
        current = self.get_current_traversal_node()
        current.set_level(0)

    def tmp(self):
        before_action = self.get_current_traversal_node()   # 操作之前的 界面节点
        open_list = before_action.get_open()  # 获取操作之前的未执行过的操作
        if open_list:  # 如果不为空，就执行操作
            window_node = open_list[0]  # 获取第一个节点元素
            action_result = self.do_action(action=window_node)
            if 'Error' in str(action_result):
                return
            after_action = self.get_current_traversal_node()  # 获取操作之后的界面节点
            if not self.is_current_window_legal(): #  判断当前节点是否合法 可能以后会在判断过程中把一些ALLOW的提醒点掉
                before_action.move_to_closed(window_node)  # 将操作步骤 从OPEN列表移动CLOSED列表
                Utility.output_msg('Current window is illegal.')
                after_action.move_all_open_to_closed() # 如果是非法的 则将这个节点里面的操作节点全部修改到closed状态
                after_action.append_previous((before_action.get_node_eigenvalue(), window_node))  # 操作的后的节点添加前继
                before_action.append_next((after_action.get_node_eigenvalue(), window_node))  # 操作后的节点添加后继
                return
            if before_action is after_action:  # 判断节点是否为同一个
                before_action.move_to_optional(window_node)
                Utility.output_msg('Interface is not changed')
            else:
                before_action.move_to_closed(window_node)  # 将操作步骤 从OPEN列表移动CLOSED列表
                Utility.output_msg('Interface has changed')
                after_action.set_level(before_action.get_level()+1)
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

    def set_current_dump_path(self):  # 更新最新的dump路径，每次调用自动加1
        self.current_dump = join(self.log_directory, '%04d.uix' % self.count)
        self.current_dump_screenshot = join(self.log_directory, '%04d.png' % self.count)
        self.current_dump_txt = join(self.log_directory, '%04d.txt' % self.count)
        self.count += 1

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

    def get_not_complete_node(self):
        for eigenvalue in self.list_eigenvalue:
            traversal_node = self.dict_traversal_node.get(eigenvalue)
            if traversal_node.get_level() > 10:
                traversal_node.move_all_open_to_closed()
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
        current_package_name = self.device.get_current_package_name()
        if current_package_name == self.package_name:
            return True
        elif current_package_name is None:
            self.device.press_recent()
            sleep(1)
            self.device.press_back()
            sleep(1)
            return self.is_current_window_legal()
        return False

if __name__ == '__main__':
    #package_name = "com.android.dialer"
    #package_name = "com.android.mms"
    #package_name = "com.tencent.token"
    #package_name = "com.tencent.qqmusic"
    #package_name = "com.android.deskclock"
    package_name = "com.letv.android.client"
    #activity_name = '.NotesList'
    #activity_name='.activity.AppStarterActivity'
    activity_name = '.activity.MainActivity'
    d = Debug(project='SDM660', package_name=package_name,activity_name=activity_name)
    d.main()