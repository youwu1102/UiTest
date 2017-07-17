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

    def main(self):
        self.initialization()
        self.processing()
        self.finish()

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

    def __restart_app(self):
        Utility.stop_process_on_device(self.package_name)
        Utility.start_process_on_device(self.package_name, self.activity_name)
        sleep(15)

    def calculated_path(self, target):
        current = self.get_current_traversal_node()
        current_eige = current.get_node_eigenvalue()
        if current_eige == target:
            return [current.get_id()], [], 0
        else:
            return self.__find_path_file(start=current_eige, end=target)



    def __read_path_file(self,file_path):
        with open(join(self.case_directory,file_path)) as r_file:
            lines = r_file.readlines()
            lines = [eval(x.strip('\n')) for x in lines]
        return lines

    def __find_path_file(self, start, end):
        start_id = self.dict_eige_mappint_id.get(start)
        end_id = self.dict_eige_mappint_id.get(end)
        for path_file in os.listdir(self.case_directory):
            path_list = path_file.replace('.txt','').split('_')
            if path_list[0] == str(start_id) and path_list[-1] == str(end_id):
                return path_list, self.__read_path_file(path_file)
            elif str(start_id) in path_list and path_list[-1] == str(end_id):
                return path_list, self.__read_path_file(path_file)
        return [start_id], []



    def get_current_eigenvalue(self):
        self.device.dump('current')
        return Analysis.calculate_eigenvalue('current')

    def depth_first_traversal(self, expect_start_eigenvalue):
        Utility.output_msg('ACTION|START')
        traversal_path, action_path, index = self.calculated_path(expect_start_eigenvalue)
        print traversal_path, action_path
        for action in action_path:
            self.do(action)
            sleep(1)
        while True:
            before_action = self.get_current_traversal_node() # 先获取当前节点信息
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
                    return
                if before_action is after_action:  # 判断节点是否为同一个
                    Utility.output_msg('ACTION|AFTER|SAME')
                    before_action.move_to_optional(window_node)
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





    def rename_case_xml(self):
        if os.path.exists(self.case_xml):
            Utility.output_msg('I find an old config file for %s, I will generate a new one.')
            for x in xrange(1, 10000):
                back_case_xml = join(self.case_directory, 'Config.xml.back%s' % x)
                if not os.path.exists(back_case_xml):
                    os.rename(self.case_xml, back_case_xml)
                    break
        return self.case_xml


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
        for value in self.dict_eige_mapping_node.values():
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


if __name__ == '__main__':
    package_name = "com.android.mms"
    activity_name = '.ui.ConversationList'
    d = Debug(project='SDM660', package_name=package_name,activity_name=activity_name)
    d.main()