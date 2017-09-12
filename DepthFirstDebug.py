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
from difflib import SequenceMatcher

class Debug(object):
    def __init__(self, project, package_name, serial=None, activity_name=''):
        self.project = project
        self.package_name = package_name
        GlobalVariable.package_name = package_name
        self.activity_name = activity_name
        self.device = UiAutomator(serial)
        self.log_directory = Utility.make_dirs(join(GlobalVariable.logs_directory, package_name))
        self.txt_directory = Utility.make_dirs(join(self.log_directory, 'Node'))
        self.case_directory = Utility.make_dirs(join(GlobalVariable.case_utils, project, package_name))
        self.current_dump = ''
        self.current_dump_txt = ''
        self.current_dump_screenshot = ''
        self.list_traversal_node = list()
        self.dict_eige_mapping_node = dict()
        self.new_node_count = 0
        self.count = 0  # 计数器
    def main(self):
        self.initialization()
        self.processing()
        self.finish()

    def finish(self):
        pass

    def initialization(self):
        Utility.run_command_on_pc('adb root')
        sleep(3)
        Utility.run_command_on_pc('adb wait-for-device')
        Utility.stop_process_on_device(self.package_name)
        Utility.start_process_on_device(self.package_name, self.activity_name)
        self.get_current_traversal_node()  # 将一个节点添加进去

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
        self.device.click(text='首页')
        sleep(5)

    def return_to_first_page(self):
        current = self.get_current_traversal_node()
        current_id = str(current.get_id())
        if current_id == '0':
            return True
        for path_file in os.listdir(self.case_directory):
            if '.opt' in path_file:
                continue
            path_list = path_file.replace('.txt', '').split('_')
            if current_id in path_list and path_list[-1] == '0':
                actions = self.__read_path_file(path_file)[path_list.index(current_id):]
                for action in actions:
                    self.do(action)
        if self.get_current_traversal_node().get_id() == 0:
            return True
        self.restart_process_on_device()
        return False


    def calculated_path(self, target):
        current = self.get_current_traversal_node()
        current_eige = current.get_eigenvalue()
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
        start_id = self.dict_eige_mapping_node.get(start).get_id()
        end_id = self.dict_eige_mapping_node.get(end).get_id()
        for path_file in os.listdir(self.case_directory):
            if '.opt' in path_file:
                continue
            path_list = path_file.replace('.txt', '').split('_')
            if path_list[0] == str(start_id) and path_list[-1] == str(end_id):
                return path_list, self.__read_path_file(path_file), 0
            if str(start_id) in path_list and path_list[-1] == str(end_id):
                print path_list.index(str(start_id))
                return path_list, self.__read_path_file(path_file), path_list.index(str(start_id))
        self.add_attempts(end)
        self.restart_process_on_device()
        current = self.get_current_traversal_node()
        return [current.get_id()], [], 0

    def add_attempts(self, eige):
        node = self.dict_eige_mapping_node.get(eige)
        node.add_attempts()

    def get_current_eigenvalue(self):
        self.device.dump('current')
        return Analysis.calculate_eigenvalue('current')

    def depth_first_traversal(self, expect_start_eigenvalue):
        #返回初始的地址
        self.return_to_first_page()
        traversal_path, action_path, index = self.calculated_path(expect_start_eigenvalue)
        for x in range(index, len(action_path)):
            self.do(action_path[x])
            sleep(1)

        #第一步走到目标位置
        while True:
            before_action = self.get_current_traversal_node() # 先获取当前节点信息
            before_action.reset_attempts()
            open_list = before_action.get_open()  # 获取操作之前的未执行过的操作
            if open_list:  # 如果不为空，就执行操作
                window_node = open_list[0]  # 获取第一个节点元素
                before_action.add_to_closed(window_node)  # 只要不出错就将节点放到关闭的状态下
                if not self.do(action=window_node):  # 判断是否出错 如果出错就返回
                    Utility.output_msg('ACTION|UIAUTOMATION|EXCEPTION')
                    self.__write_path_optional(traversal_path, action_path, window_node)
                    return
                after_action = self.get_current_traversal_node()  # 获取操作之后的界面节点
                if before_action is after_action:  # 判断节点是否为同一个
                    Utility.output_msg('ACTION|AFTER|SAME')
                    self.__write_path_optional(traversal_path, action_path, window_node)
                    continue

                if after_action.get_type() == 'illegal':  # 判断当前节点是否合法 不合法就写饭之后返回最后界面
                    traversal_path.append(after_action.get_id())
                    action_path.append(window_node)
                    self.__write_path(traversal_path, action_path)
                    self.return_to_normal_package()
                    return

                if after_action.get_id() in traversal_path:  # 如果执行路径中已经存在了 就返回
                    print traversal_path
                    traversal_path.append(after_action.get_id())
                    print traversal_path
                    action_path.append(window_node)
                    self.__write_path(traversal_path, action_path)
                    return

                Utility.output_msg('ACTION|AFTER|NORMAL')
                traversal_path.append(after_action.get_id())
                action_path.append(window_node)
                self.__write_path(traversal_path, action_path)
            else:
                return
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
        sleep(1)
        self.dump_current_window()
        current_eigenvalue, current_window_nodes = Analysis.get_info_from_dump(self.current_dump)
        if not self.compare_node_exists(current_eigenvalue, current_window_nodes):
            current_traversal_node = TraversalNode(current_eigenvalue) # 初始化node
            current_traversal_node.init_total(current_window_nodes)  # 初始化 node中的节点
            current_traversal_node.set_id(self.new_node_count)    # 初始化 node ID
            self.__write_node(current_traversal_node)  # 方便写出来查看 可以不用
            self.dict_eige_mapping_node[current_eigenvalue] = current_traversal_node
            self.list_traversal_node.append(current_traversal_node)
            self.new_node_count += 1
        else:
            current_traversal_node = self.dict_eige_mapping_node.get(current_eigenvalue)
        return current_traversal_node

    def compare_node_exists(self, eigenvalue, window_nodes):
        for p_eigenvalue in self.dict_eige_mapping_node.keys():  # 之前出现过的NODE列表
            p_node = self.dict_eige_mapping_node.get(p_eigenvalue)
            compare_result = Debug.compare_eigenvalue(eigenvalue, p_eigenvalue)
            print compare_result
            if compare_result == 'same':   # 如果比较结果是完全一样的 则返回True
                return True
            elif compare_result == 'almost':  # 如果比较结果几乎一样，就需要合并两个node,然后返回结果
                print p_node.get_id()
                self.__modify_node(id=p_node.get_id(), eigenvalue=eigenvalue, window_nodes=window_nodes)
                p_node.merge_total(window_nodes=window_nodes)
                self.dict_eige_mapping_node[eigenvalue] = p_node
                return True
        return False


    @staticmethod
    def compare_eigenvalue(x, y):
        if x == y:  # 完全相等
            return 'same'
        else:
            same_number = Debug.same_between_eigenvalue(str1=x, str2=y) * 1.0
            compare_x = same_number / len(x)
            compare_y = same_number / len(y)
            if compare_x > 0.95 and compare_y >= 0.85:
                return 'almost'
            elif compare_y > 0.95 and compare_x >= 0.85:
                return 'almost'
            elif compare_x >= 0.9 and compare_y >=0.9:
                return 'almost'
        return 'not_same'

    @staticmethod
    def same_between_eigenvalue(str1, str2):
        total = 0
        test = SequenceMatcher(None, str1, str2)
        for block in test.get_matching_blocks():
            total += block.size
        return total

    def get_not_complete_node(self):
        for attempts_limit in range(3):
            for traversal_node in self.list_traversal_node:
                if not self.traversal_node_rule(traversal_node=traversal_node, attempts_limit=attempts_limit):
                    continue
                return traversal_node.get_eigenvalue()
        return None

    def traversal_node_rule(self, traversal_node, attempts_limit):
        if traversal_node.get_type() == 'illegal':
            return False
        if traversal_node.get_attempts() > attempts_limit:
            return False
        open_list = traversal_node.get_open()
        if not open_list:  # 判断是否还有open的节点
            return False
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

    def return_to_normal_package(self):
        for x in range(10):
            self.device.press_back()
            self.device.click_if_exists(text='ALLOW')
            if self.device.get_current_package_name() == self.package_name:
                break


    def __write_path(self,traversal_path, action_path):
        tmp = [str(x) for x in traversal_path]
        file_name = '_'.join(tmp)
        with open(join(self.case_directory, file_name+'.txt'), 'w') as w_file:
            for action in action_path:
                w_file.write(str(action)+'\n')

    def __write_path_optional(self,traversal_path, action_path, window_node):
        tmp = [str(x) for x in traversal_path]
        file_name = '_'.join(tmp)
        with open(self.__get_option_name(file_name), 'w') as w_file:
            for action in action_path:
                w_file.write(str(action)+'\n')
            w_file.write(str(window_node) + '\n')

    def __get_option_name(self, file_name):
        tmp_path = join(self.case_directory, file_name+'.opt')
        for x in xrange(1, 10000):
            tmp = tmp_path + str(x)
            if not os.path.exists(tmp):
                return tmp
        return join(self.case_directory, 'Exception.txt')

    def __write_node(self, node):
        with open(join(self.txt_directory, '%d.txt' % node.get_id()), 'w') as w_file:
            w_file.write(node.get_eigenvalue()+'\n')
            for open_action in node.get_open():
                w_file.write(str(open_action)+'\n')
            w_file.write('\n')
            w_file.write(self.current_dump+'\n')
            w_file.write(self.current_dump_screenshot+'\n')
            w_file.write('\n\n')

    def __modify_node(self, id, eigenvalue, window_nodes):
        with open(join(self.txt_directory, '%d.txt' % id)) as r_file:
            if eigenvalue in r_file.read():
                return True
        with open(join(self.txt_directory, '%d.txt' % id), 'a+') as w_file:
            w_file.write(eigenvalue+'\n')
            for open_action in window_nodes:
                w_file.write(str(open_action)+'\n')
            w_file.write('\n')
            w_file.write(self.current_dump+'\n')
            w_file.write(self.current_dump_screenshot+'\n')
            w_file.write('\n\n')

if __name__ == '__main__':
    package_name = "com.tencent.mm"
    activity_name = '.ui.LauncherUI'
    # package_name = "org.codeaurora.snapcam"
    # activity_name = 'com.android.camera.CameraActivity'
    d = Debug(project='SDM660', package_name=package_name,activity_name=activity_name)
    d.main()