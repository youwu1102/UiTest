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

    @staticmethod
    def __node_useless_rule(node):
        if node.get('clickable') == 'true':
            node['action'] = 'Click'
            return False

        # elif 'android.widget.EditText' == node.get('class'):
        #     return False
        return True


class Analysis(object):
    @staticmethod
    def calculate_eigenvalue(dump_path):
        eigenvalue = Eigenvalue.calculate_eigenvalue(dump_path=dump_path)
        Utility.output_msg('Tbe current dump eigenvalue is:%s' % eigenvalue)
        return eigenvalue

    @staticmethod
    def get_info_from_dump(dump_path):
        Utility.output_msg('I will analysis the dump file: %s' % dump_path)
        eigenvalue = Eigenvalue.calculate_eigenvalue(dump_path)
        Utility.output_msg('I got the eigenvalue: %s ' % eigenvalue)
        window_nodes = Analysis.get_nodes_from_dump(dump_path)
        Utility.output_msg('I got the window nodes:', 'd')
        for node in window_nodes:
            Utility.output_msg(str(node), 'd')
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
        return dump_nodes

