# -*- encoding:UTF-8 -*-

from Eigenvalue import Eigenvalue
from Utility import Utility
from GlobalVariable import GlobalVariable
from xml.dom import minidom
__author__ = 'c_youwu'


class Nodes(object):
    @staticmethod
    def remove_useless_nodes(nodes):   # 留下有用的NODE 并且将操作写进去
        tmp_nodes = nodes[:]
        for node in tmp_nodes:
            if Nodes.__node_useless_rule(node):
                nodes.remove(node)
        tmp_nodes = nodes[:]



    @staticmethod
    def __node_useless_rule(node):
        # if node.get('class') == 'android.widget.FrameLayout':
        #     return False
        # if node.get('class') == 'android.widget.LinearLayout':
        #     return False
        if node.get('clickable') == 'true':
            node['action'] = 'Click'
            return False
        return True


class Analysis(object):
    @staticmethod
    def calculate_eigenvalue(dump_path):
        eigenvalue = Eigenvalue.calculate_eigenvalue(dump_path=dump_path)
        return eigenvalue

    @staticmethod
    def get_info_from_dump(dump_path):
        eigenvalue = Eigenvalue.calculate_eigenvalue(dump_path)
        Utility.output_msg('WINDOW|EIGE:%s ' % eigenvalue)
        window_nodes = Analysis.get_nodes_from_dump(dump_path)
        Utility.output_msg('WINDOW|NODE:%s' % len(window_nodes))
        return eigenvalue, window_nodes

        # if eigenvalue not in GlobalVariable.dict_E_M_N.keys():
        #     Utility.output_msg('This eigenvalue has not appeared before.')
        #     node = TraversalNode(eigenvalue)
        #     node.append_previous()
        #     node.init_open(Utility.__get_actions_from_dump(dump_path))
        #     GlobalVariable.dict_E_M_N[eigenvalue] = node
        # else:
        #     Utility.output_msg('This eigenvalue has appeared before.')
        # return eigenvalue

    @staticmethod
    def get_nodes_from_dump(dump_path):
        nodes = Analysis.__get_nodes_from_dump(dump_path)
        actions = Analysis.__category_nodes(nodes)
        return actions

    @staticmethod
    def __get_nodes_from_dump(dump_path):
        node_list = []
        dom = minidom.parse(dump_path)
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        for node in nodes:
            dict_node = {}
            for attr in GlobalVariable.list_attrs:
                dict_node[attr] = node.getAttribute(attr)
            node_list.append(dict_node)
        return node_list

    @staticmethod
    def __category_nodes(dump_nodes):  # 分类节点，将有用的留下 删除没用的
        Nodes.remove_useless_nodes(dump_nodes)
        window_nodes = list()
        for node in dump_nodes:
            action = Analysis.get_selector(node)
            action['action'] = node.get('action')
            if action not in window_nodes:
                window_nodes.append(action)
        return window_nodes

    list_selector = ['text', 'resource-id', 'content-desc', 'class', 'index']

    @staticmethod
    def get_selector(action):
        dict_tmp = dict()
        dict_tmp['package'] = action.get('package')
        text = action.get('text')
        if text:
            dict_tmp['text'] = text
            return dict_tmp
        desc = action.get('content-desc')
        if desc:
            dict_tmp['content-desc'] = desc
            return dict_tmp
        for key in Analysis.list_selector:
            key_value = action.get(key)
            if key_value:
                dict_tmp[key] = key_value
        return dict_tmp