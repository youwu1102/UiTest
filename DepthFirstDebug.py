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
        self.txt_directory = Utility.make_dirs(join(self.log_directory, 'Node'))
        self.case_directory = Utility.make_dirs(join(GlobalVariable.case_utils, project, package_name))
        self.current_dump = ''
        self.current_dump_txt = ''
        self.current_dump_screenshot = ''
        self.dict_eige_mapping_node = dict()  # 每一个特征值对应一个遍历路径上的节点
        self.dict_id_mappint_eige = dict()
        self.dict_eige_mappint_id = dict()
        self.list_eige = list()  # 记录遍历节点出现的顺序
        self.dict_path_mapping_action = dict()
        self.new_node_count = 0
        self.count = 0  # 计数器
        self.return_count=0

    def main(self):
        self.initialization()
        self.processing()
        self.finish()

    def finish(self):
        pass

    def initialization(self):
        Utility.stop_process_on_device(self.package_name)
        Utility.start_process_on_device(self.package_name, self.activity_name)
        current = self.get_current_traversal_node()
        current.set_level(0)

    def processing(self):
        Utility.output_msg('PROCESSING|START')
        while True:
            Utility.output_msg('PROCESSING|WHILE:START')
            eigenvalue = self.get_not_complete_node()
            if eigenvalue:# 判断是否全部结束了 没有再出现新节点
                self.depth_first_traversal(eigenvalue)   #无论是否找到  都会执行一步操作
            else:
                Utility.output_msg('All locations have been traversed.')
                break
            Utility.output_msg('PROCESSING|WHILE:END')
        Utility.output_msg('PROCESSING|END')


    def restart_process_on_device(self):
        Utility.stop_process_on_device(self.package_name)
        Utility.start_process_on_device(self.package_name, self.activity_name)
        sleep(5)

    def calculated_path(self, target):

        current = self.get_current_traversal_node()
        current_eige = current.get_node_eigenvalue()
        if current_eige == target:
            return [current.get_id()], [], 0
        else:
            return self.__find_path_file(start=current_eige, end=target)

    def calculated_path_1(self, target):
        current = self.get_current_traversal_node()
        current_eige = current.get_node_eigenvalue()
        if current_eige == target:
            return [current.get_id()], [], 0
        else:
            return self.__find_path_file(start=current_eige, end=target)


    def __read_path_file(self, file_path):
        with open(join(self.case_directory,file_path)) as r_file:
            lines = r_file.readlines()
            lines = [eval(x.strip('\n')) for x in lines]
        return lines

    def __find_path_file(self, start, end):
        start_id = self.dict_eige_mappint_id.get(start)
        end_id = self.dict_eige_mappint_id.get(end)
        for path_file in os.listdir(self.case_directory):
            if '.opt' in path_file:
                continue
            path_list = path_file.replace('.txt', '').split('_')
            if str(start_id) in path_list and path_list[-1] == str(end_id):
                print path_list.index(str(start_id))
                return path_list, self.__read_path_file(path_file), path_list.index(str(start_id))
        self.add_attempts(end)
        self.restart_process_on_device()
        current = self.get_current_traversal_node()
        return [self.dict_eige_mappint_id.get(current)], [], 0

    def add_attempts(self, eige):
        node = self.dict_eige_mapping_node.get(eige)
        node.add_attempts()

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
                return False
            sleep(0.5)
        Utility.output_msg('Function return_to_expect_location over.', 'd')
        return True

    def get_current_eigenvalue(self):
        self.device.dump('current')
        return Analysis.calculate_eigenvalue('current')

    def depth_first_traversal(self, expect_start_eigenvalue):
        Utility.output_msg('ACTION|START')
        traversal_path, action_path, index = self.calculated_path(expect_start_eigenvalue)
        print traversal_path, action_path
        for x in range(index, len(action_path)):
            self.do(action_path[x])
            sleep(1)
        while True:
            before_action = self.get_current_traversal_node() # 先获取当前节点信息
            before_action.reset_attempts()
            open_list = before_action.get_open()  # 获取操作之前的未执行过的操作
            Utility.output_msg('ACTION|BEFORE|NODE|EIGI:%s' % before_action.get_node_eigenvalue())
            Utility.output_msg('ACTION|BEFORE|NODE|OPEN:%s' % len(before_action.get_open()))
            if open_list:  # 如果不为空，就执行操作
                window_node = open_list[0]  # 获取第一个节点元素
                if not self.do(action=window_node):
                    Utility.output_msg('ACTION|UIAUTOMATION|EXCEPTION')
                    return
                sleep(1)
                after_action = self.get_current_traversal_node()  # 获取操作之后的界面节点
                Utility.output_msg('ACTION|AFTER|NODE|EIGI:%s' % after_action.get_node_eigenvalue())
                Utility.output_msg('ACTION|AFTER|NODE|OPEN:%s' % len(after_action.get_open()))
                if not self.is_current_window_legal():  # 判断当前节点是否合法
                    Utility.output_msg('ACTION|AFTER|ILLEGAL')
                    before_action.move_to_closed(window_node)  # 将操作步骤 从OPEN列表移动CLOSED列表
                    after_action.set_level(before_action.get_level() + 1)
                    after_action.move_all_open_to_optional()  # 如果是非法的 则将这个节点里面的操作节点全部修改到closed状态
                    after_action.append_previous((before_action.get_node_eigenvalue(), window_node))  # 操作的后的节点添加前继
                    before_action.append_next((after_action.get_node_eigenvalue(), window_node))  # 操作后的节点添加后继
                    traversal_path.append(after_action.get_id())
                    action_path.append(window_node)
                    self.__write_path(traversal_path, action_path)
                    self.return_to_normal_package()
                    return
                if before_action is after_action:  # 判断节点是否为同一个
                    Utility.output_msg('ACTION|AFTER|SAME')
                    before_action.move_to_optional(window_node)
                    self.__write_path_optional(traversal_path, action_path, window_node)
                    continue
                else:
                    Utility.output_msg('ACTION|AFTER|NORMAL')
                    before_action.move_to_closed(window_node)  # 将操作步骤 从OPEN列表移动CLOSED列表
                    after_action.set_level(before_action.get_level() + 1)
                    after_action.append_previous((before_action.get_node_eigenvalue(), window_node))  # 操作的后的节点添加前继
                    before_action.append_next((after_action.get_node_eigenvalue(), window_node))  # 操作后的节点添加后继

                if after_action.get_id() in traversal_path: # 如果执行路径中已经存在了 就返回
                    traversal_path.append(after_action.get_id())
                    action_path.append(window_node)
                    self.__write_path(traversal_path, action_path)
                    return

                traversal_path.append(after_action.get_id())
                action_path.append(window_node)
                self.__write_path(traversal_path, action_path)
            else:
                return
        Utility.output_msg('ACTION|END')


    def __write_path(self,traversal_path, action_path):
        tmp = [str(x) for x in traversal_path]
        file_name = '_'.join(tmp)
        with open(join(self.case_directory, file_name+'.txt'), 'w') as w_file:
            for action in action_path:
                w_file.write(str(action)+'\n')

    def __write_path_optional(self,traversal_path, action_path, window_node):
        tmp = [str(x) for x in traversal_path]
        file_name = '_'.join(tmp)
        with open(self.get_option_name(file_name), 'w') as w_file:
            for action in action_path:
                w_file.write(str(action)+'\n')
            w_file.write(str(window_node) + '\n')

    def get_option_name(self, file_name):
        tmp_path = join(self.case_directory, file_name+'.opt')
        for x in xrange(1, 10000):
            tmp = tmp_path + str(x)
            if not os.path.exists(tmp):
                return tmp
        return False

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
        if current_eigenvalue not in self.dict_eige_mapping_node.keys():
            Utility.output_msg('SYSTEM|NEW:%s' % current_eigenvalue)
            current_traversal_node = TraversalNode(current_eigenvalue) # 初始化node
            current_traversal_node.init_open(current_window_nodes)  # 初始化 node中的节点
            current_traversal_node.set_id(self.new_node_count)    # 初始化 node ID
            self.__write_node(current_traversal_node)  # 方便写出来查看 可以不用
            self.dict_eige_mappint_id[current_eigenvalue] = self.new_node_count
            self.dict_id_mappint_eige[self.new_node_count] = current_eigenvalue
            self.dict_eige_mapping_node[current_eigenvalue] = current_traversal_node
            self.list_eige.append(current_eigenvalue)
            self.new_node_count += 1
        else:
            Utility.output_msg('SYSTEM|GET:%s' % current_eigenvalue)
            current_traversal_node = self.dict_eige_mapping_node.get(current_eigenvalue)
        return current_traversal_node

    def get_not_complete_node(self):
        for attempts_limit in range(3):
            for eigenvalue in self.list_eige:
                traversal_node = self.dict_eige_mapping_node.get(eigenvalue)
                if not self.traversal_node_rule(traversal_node=traversal_node, attempts_limit=attempts_limit):
                    continue
                open_list = traversal_node.get_open()
                if open_list:
                    Utility.output_msg('NOT_COMPLETE|NODE|EIGE:%s' % traversal_node.get_node_eigenvalue())
                    Utility.output_msg('NOT_COMPLETE|NODE|OPEN:%s' % len(open_list))
                    Utility.output_msg('NOT_COMPLETE|NODE|A:%s' % traversal_node.get_attempts())
                    Utility.output_msg('NOT_COMPLETE|NODE|L:%s' % traversal_node.get_level())
                    # for o in open_list:
                    #     Utility.output_msg('NOT_COMPLETE|NODE| ACT:%s' % str(o))
                    return traversal_node.get_node_eigenvalue()
        return None

    def __write_node(self, node):
        with open(join(self.txt_directory, '%d.txt' % node.get_id()), 'w') as w_file:
            w_file.write(node.get_node_eigenvalue()+'\n')
            for open_action in node.get_open():
                w_file.write(str(open_action)+'\n')
            w_file.write('\n\n')
            w_file.write(self.current_dump+'\n')
            w_file.write(self.current_dump_screenshot+'\n')

    def traversal_node_rule(self, traversal_node, attempts_limit):
        open_list = traversal_node.get_open()
        if not open_list:  # 判断是否还有open的节点
            return False
        if traversal_node.get_level() > 5:  # 判断遍历层次是否大于10
            traversal_node.move_all_open_to_closed()
            return False
        if traversal_node.get_attempts() > attempts_limit:
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

    def return_to_normal_package(self):
        for x in range(10):
            self.device.press_back()
            if self.device.get_current_package_name() == self.package_name:
                break

if __name__ == '__main__':
    package_name = "com.kugou.android"
    activity_name = '.app.MediaActivity'
    package_name = "com.android.mms"
    activity_name = '.ui.ConversationList'
    d = Debug(project='SDM660', package_name=package_name,activity_name=activity_name)
    d.main()