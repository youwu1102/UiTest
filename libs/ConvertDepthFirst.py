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

    def text_to_xml(self, path):
        self.parse_txt(path)
        self.write_xml(Utility.make_dirs(os.path.join(path, 'Cases')))

    def write_xml(self,save_path):
        count = 1
        for case in self.cases:
            doc = Document()
            root = doc.createElement('case')
            for action in case:
                action_node = doc.createElement('action')
                action_node.setAttribute('name', 'click')
                action_node.setAttribute('clickable', 'true')
                if action.get('text'):
                    action_node.setAttribute('text', action.get('text'))
                if action.get('content-desc'):
                    action_node.setAttribute('desc', action.get('content-desc'))
                if action.get('resource-id'):
                    action_node.setAttribute('id', action.get('resource-id'))
                if action.get('class'):
                    action_node.setAttribute('class', action.get('class'))
                if action.get('index'):
                    action_node.setAttribute('index', action.get('index'))
                root.appendChild(action_node)
            doc.appendChild(root)
            f = open(os.path.join(save_path, '%s.xml' % count), 'w')
            f.write(doc.toprettyxml(indent='', encoding='utf-8'))
            f.close()
            count+=1

    def parse_txt(self, path):
        for path_file in os.listdir(path):
            if path_file=='Cases':
                continue
            with open(join(path, path_file)) as r_file:
                actions = []
                lines = r_file.readlines()
                for line in lines:
                    actions.append(self.convert_line_to_selector(line))
            if actions not in self.cases and len(actions) > 6:
                self.cases.append(actions)

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
    c.text_to_xml('C:\cygwin64\home\c_youwu\UiTest\\repository\CaseUtils\SDM660\com.kugou.android\\')

