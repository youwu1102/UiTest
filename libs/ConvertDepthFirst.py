__author__ = 'c_youwu'
import os
from os.path import join
from xml.dom.minidom import Document
from Utility import Utility


class Convert(object):
    def __init__(self):
        self.cases = list()
        self.dict_selector = {'text': 'text',
                     'resource-id': 'id',
                     'content-desc': 'desc',
                     'class': 'class',
                     'index': 'index'}
        self.dict_node = dict()
    def text_to_xml(self, path):
        self.parse_path_to_node(path)
        self.parse_path_to_cases(path)
        self.write_cases_to_xml(Utility.make_dirs(os.path.join(path, 'Cases')))




    def write_cases_to_xml(self,save_path):
        count = 1
        self.cases = sorted(self.cases)
        for case in self.cases:
            doc = Document()
            root = doc.createElement('case')
            for action in case:
                action= eval(action)
                action_node = doc.createElement('action')
                action_node.setAttribute('name', 'click')
                action_node.setAttribute('clickable', 'true')
                if action.get('text'):
                    action_node.setAttribute('text', action.get('text'))
                if action.get('desc'):
                    action_node.setAttribute('desc', action.get('desc'))
                if action.get('id'):
                    action_node.setAttribute('id', action.get('id'))
                if action.get('class'):
                    action_node.setAttribute('class', action.get('class'))
                if action.get('index'):
                    action_node.setAttribute('index', action.get('index'))
                root.appendChild(action_node)
            doc.appendChild(root)
            f = open(os.path.join(save_path, '%04d.xml' % count), 'w')
            f.write(doc.toprettyxml(indent='', encoding='utf-8'))
            f.close()
            count+=1

    def parse_path_to_node(self, path):
        for path_file in os.listdir(path):
            if path_file == 'Cases':
                continue
            if path_file[0] not in ['0']:
                continue
            if '.opt' in path_file:
                traversal_path = path_file[:path_file.index('.')]
                traversal_list = traversal_path.split('_')
                for x in range(len(traversal_list)):
                    member = traversal_list[x]
                    action = self.get_actions(join(path,path_file))[x]
                    if not self.dict_node.get(member):
                        self.dict_node[member] = list()
                    if action not in self.dict_node.get(member):
                        self.dict_node.get(member).append(action)
            else:
                traversal_path = path_file[:path_file.index('.')]
                traversal_list = traversal_path.split('_')
                for x in range(len(traversal_list)-1):
                    member = traversal_list[x]
                    action = self.get_actions(join(path,path_file))[x]
                    if not self.dict_node.get(member):
                        self.dict_node[member] = list()
                    if action not in self.dict_node.get(member):
                        self.dict_node.get(member).append(action)

    def parse_path_to_cases(self,path):
        for path_file in os.listdir(path):
            if path_file == 'Cases':
                continue
            if path_file[0] not in ['0', '11']:
                continue
            traversal_path = path_file[:path_file.index('.')]
            traversal_list = traversal_path.split('_')
            last_node = traversal_list[-1]
            with open(join(path, path_file)) as r_file:
                actions = []
                lines = r_file.readlines()
                for line in lines:
                    actions.append(str(self.convert_line_to_selector(line)))
            if not self.compare_case_if_exist(case=actions):
                print len(actions)
                self.cases.append(actions)

    def compare_case_if_exist(self, case):
        if case in self.cases:
            return True
        for x in range(len(self.cases)):
            if set(self.cases[x]) > set(case):
                return True
            elif set(case) > set(self.cases[x]):
                self.cases[x] = case
                return True
        if len(case) < 2:
            return True
        return False

    def get_actions(self,path):
        with open(path) as r_file:
            actions = []
            lines = r_file.readlines()
            for line in lines:
                actions.append(self.convert_line_to_selector(line))
        return actions

    def convert_line_to_selector(self, line):
        dict_line = eval(line)
        dict_tmp = dict()
        text = dict_line.get('text')
        if text:
            dict_tmp['text'] = text
            return dict_tmp
        desc = dict_line.get('content-desc')
        if desc:
            dict_tmp['desc'] = desc
            return dict_tmp
        for key in self.dict_selector.keys():
            key_value = dict_line.get(key)
            if key_value:
                dict_tmp[self.dict_selector.get(key)] = key_value
        return dict_tmp


if __name__ == '__main__':
    c =Convert()
    c.text_to_xml('C:\cygwin64\home\c_youwu\UiTest\\repository\CaseUtils\SDM660\\com.tencent.mm\\')

