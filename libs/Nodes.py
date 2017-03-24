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
        if node.get('clickable') == 'true':
            return False
        elif 'android.widget.EditText' == node.get('class'):
            return False
        return True

    @staticmethod
    def convert_to_actions(nodes):
        actions = []
        tmp_nodes = nodes[:]
        for node in tmp_nodes:
            clickable = node.get('clickable')
            if clickable == 'true':
                text = node.get('text')
                r_id = node.get('resource-id')
                desc = node.get('content-desc')
                _class = node.get('class')
                action_list = ['CLICK', '', text, r_id, desc, _class]
                action_string = ',\t'.join(action_list)
                action = '%04d,\t' % (6+len(action_string)) + action_string
                nodes.remove(node)
                actions.append([action])
        return actions
