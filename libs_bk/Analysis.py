# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
from parse_xml import ParseXML
import time
start = time.time()


class Analysis(object):
    common_p1, common_p2, common_p3 = ParseXML.parse_priority_config('C:\Users\c_youwu\Desktop\UiTest\configs\Common.xml')
    forum_p1, forum_p2, forum_p3 = ParseXML.parse_priority_config('C:\Users\c_youwu\Desktop\UiTest\configs\Forum.xml')
    forum_p1 = dict(forum_p1, **common_p1)
    forum_p2 = dict(forum_p2, **common_p2)
    forum_p3 = dict(forum_p3, **common_p3)

    @staticmethod
    def ui_dump(dump_path, app_type):
        dict_dump_result = dict()
        dict_dump_result['Path'] = dump_path
        nodes = ParseXML.parse_ui_dump_xml(xml_path=dump_path)
        Analysis.parse_to_actions(nodes=nodes, priority_tuple=Analysis.switch_app_type(app_type=app_type),
                                  dict_dump=dict_dump_result)
        return dict_dump_result

    @staticmethod
    def clear_useless_node(nodes):
        tmp_nodes = nodes[:]
        for node in tmp_nodes:
            if Analysis.__useless_rule(node=node):
                nodes.remove(node)

    @staticmethod
    def __useless_rule(node):
        if node.get('class') in ['android.widget.LinearLayout',
                                 'android.widget.RelativeLayout',
                                 'android.widget.FrameLayout']:
            if node.get('checkable') == node.get('clickable') == node.get('scrollable') == 'false':
                return True
        return False

    @staticmethod
    def parse_to_actions(nodes, priority_tuple, dict_dump):
        p1, p2, p3 = priority_tuple
        Analysis.clear_useless_node(nodes=nodes)
        list_action = []
        # print len(nodes)
        Analysis.get_actions(nodes=nodes, priority=p1, dump_path=dict_dump.get('Path'), action_list=list_action)
        Analysis.get_actions(nodes=nodes, priority=p2, dump_path=dict_dump.get('Path'), action_list=list_action)
        Analysis.get_actions(nodes=nodes, priority=p3, dump_path=dict_dump.get('Path'), action_list=list_action)
        Analysis.get_actions(nodes=nodes, priority={}, dump_path=dict_dump.get('Path'), action_list=list_action)
        # print list_action
        dict_dump['Action'] = list_action
        # for node in nodes:
        #     print node
        # print len(nodes)

    @staticmethod
    def convert_node_to_action(nodes, priority):
        ui_actions = []
        tmp_nodes = nodes[:]
        if priority:
            for mapping in priority:
                # print mapping
                m_string = mapping.get('string')
                m_action = mapping.get('action')
                m_value = mapping.get('value')
                if m_action == 'click':
                    for node in tmp_nodes:
                        text = node.get('text')
                        r_id = node.get('resource-id')
                        desc = node.get('content-desc')
                        click = node.get('clickable')
                        _class = node.get('class')
                        if (m_string in text or m_string in r_id or m_string in desc) and click == 'true':
                            action_list = ['CLICK', '', text, r_id, desc, _class]
                            action_string = ',\t'.join(action_list)
                            action = '%04d,\t' % (6+len(action_string)) + action_string
                            nodes.remove(node)
                            ui_actions.append([action])
        else:
            for node in tmp_nodes:
                clickable = node.get('clickable')
                scrollable = node.get('scrollable')
                if clickable == 'true':
                    text = node.get('text')
                    r_id = node.get('resource-id')
                    desc = node.get('content-desc')
                    _class = node.get('class')
                    action_list = ['CLICK', '', text, r_id, desc, _class]
                    action_string = ',\t'.join(action_list)
                    action = '%04d,\t' % (6+len(action_string)) + action_string
                    # print action
                    try:
                        nodes.remove(node)
                    except Exception:
                        pass
                    ui_actions.append([action])
                if scrollable == 'true':
                    print 'Find scrollable and class name :%s ' % node.get('class')
                    try:
                        nodes.remove(node)
                    except Exception:
                        pass


        return ui_actions

    @staticmethod
    def get_actions(nodes, priority, dump_path, action_list):
        if priority and nodes:
            dump_content = Analysis.get_dump_content(dump_path=dump_path)
            for key in priority.keys():
                if key in dump_content:
                    action_list.extend(Analysis.convert_node_to_action(nodes=nodes, priority=priority.get(key)))
        else:
            if nodes:
                action_list.extend(Analysis.convert_node_to_action(nodes=nodes, priority=None))


    @staticmethod
    def get_dump_content(dump_path):
        dump_file = open(dump_path)
        dump_content = dump_file.read()
        dump_file.close()
        return dump_content.decode('utf-8')

    @staticmethod
    def switch_app_type(app_type):
        if app_type == 'Forum':
            return Analysis.forum_p1, Analysis.forum_p2, Analysis.forum_p3
        else:
            return Analysis.common_p1, Analysis.common_p2, Analysis.common_p3



if __name__ == '__main__':
    Analysis.ui_dump(dump_path='C:\Users\c_youwu\Desktop\UiTest\logs\\tmp\\1.xml', app_type='Forum')

    end = time.time()
    print end-start

