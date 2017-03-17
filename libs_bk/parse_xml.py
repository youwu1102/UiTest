# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
from xml.dom import minidom


class ParseXML(object):
    @staticmethod
    def parse_priority_config(xml_path):
        dom = minidom.parse(xml_path)
        root = dom.documentElement
        # priority = dict()
        # priority['level1'] = ParseXML.__get_dict_of_level(root=root, level_name='level1')
        # priority['level2'] = ParseXML.__get_dict_of_level(root=root, level_name='level2')
        # priority['level3'] = ParseXML.__get_dict_of_level(root=root, level_name='level3')
        # return priority
        dict_level1 = ParseXML.__get_dict_of_level(root=root, level_name='level1')
        dict_level2 = ParseXML.__get_dict_of_level(root=root, level_name='level2')
        dict_level3 = ParseXML.__get_dict_of_level(root=root, level_name='level3')
        return dict_level1, dict_level2, dict_level3

    @staticmethod
    def __get_dict_of_level(root, level_name):
        dict_of_level = dict()
        level = root.getElementsByTagName(level_name)[0]
        keys = level.getElementsByTagName('search')
        for key in keys:
            mappings = key.getElementsByTagName('mapping')
            list_of_mapping = []
            for mapping in mappings:
                dict_mapping = dict()
                dict_mapping['string'] = mapping.getAttribute('string')
                dict_mapping['value'] = mapping.getAttribute('value')
                dict_mapping['action'] = mapping.getAttribute('action')
                list_of_mapping.append(dict_mapping)
            dict_of_level[key.getAttribute('string')] = list_of_mapping
        return dict_of_level

    @staticmethod
    def parse_switch_config(xml_path):
        dict_switch = dict()
        dom = minidom.parse(xml_path)
        root = dom.documentElement
        apps = root.getElementsByTagName('app')
        for app in apps:
            dict_switch[app.getAttribute('packagename')] = app.getAttribute('type')
        return dict_switch

    @staticmethod
    def parse_ui_dump_xml(xml_path):
        node_list = []
        attrs = ['index', 'text', 'resource-id', 'package', 'content-desc', 'checkable', 'checked',
                 'clickable', 'enabled', 'focusable', 'focused', 'scrollable', 'long-clickable',
                 'password', 'selected', 'bounds', 'class']
        dom = minidom.parse(xml_path)
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        for node in nodes:
            dict_node = {}
            for attr in attrs:
                dict_node[attr] = node.getAttribute(attr)
            node_list.append(dict_node)
        return node_list



if __name__ == '__main__':
    import time
    start = time.time()
    for x in xrange(1, 16):
        list_of_node = ParseXML.parse_ui_dump_xml('C:\Users\c_youwu\Desktop\UiTest\logs\\tmp\\%s.xml' % x)
        print len(list_of_node)
    end = time.time()
    print end-start
