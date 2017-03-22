__author__ = 'c_youwu'


class Nodes(object):

    @staticmethod
    def remove_useless_nodes(nodes):
        tmp_nodes = nodes[:]
        for node in tmp_nodes:
            if Nodes.__node_useless_rule(node):
                nodes.remove(node)

    @staticmethod
    def __node_useless_rule(node):
        print node
        if node.get('clickable') == 'true':
            return False

        return True