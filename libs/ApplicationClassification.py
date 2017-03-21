__author__ = 'c_youwu'
from Utility import Utility
from Eigenvalue import Eigenvalue
from xml.dom import minidom
import threading
import thread
from ADB import Adb
from GlobalVariable import GlobalVariable

class ApplicationClassification(threading.Thread):
    dict_high_priority = dict()
    dict_blacklist = dict()
    dict_dump_actions = dict()
    list_attrs = ['index', 'text', 'resource-id', 'package', 'content-desc', 'checkable', 'checked',
                  'clickable', 'enabled', 'focusable', 'focused', 'scrollable', 'long-clickable',
                  'password', 'selected', 'bounds', 'class']
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        thread.start_new_thread(ApplicationClassification.push_actions_to_device, (GlobalVariable.blank_action_file,))

    @staticmethod
    def pull_dump_to_pc(local):
        Utility.run_command_on_pc(Adb.pull(remote='/data/local/tmp/current.xml', local=local))

    @staticmethod
    def push_actions_to_device(local):
        Utility.run_command_on_pc(Adb.push(local=local, remote='/data/local/tmp/Action.txt'))

    @staticmethod
    def write_action_file():
        pass

    @staticmethod
    def analysis_dump(dump_path):
        dump_content = Utility.open_dump(dump_path)
        eigenvalue = Eigenvalue.calculate_eigenvalue(dump_content)
        if eigenvalue not in ApplicationClassification.dict_dump_actions.keys():
            ApplicationClassification.dict_dump_actions[eigenvalue] = dump_path
            nodes = ApplicationClassification.get_nodes_from_dump(dump_path)


        else:

            print dump_path
            print 'is same as:'+ ApplicationClassification.dict_dump_actions.get(eigenvalue)
            print '==========================================================='

    @staticmethod
    def get_nodes_from_dump(dump_path):
        node_list = []
        dom = minidom.parse(dump_path)
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        for node in nodes:
            dict_node = {}
            for attr in ApplicationClassification.list_attrs:
                dict_node[attr] = node.getAttribute(attr)
            node_list.append(dict_node)
        return node_list

    @staticmethod
    def convert_nodes_to_actions(nodes):
        for node in nodes:
            if node.get('checked') == 's':
                pass



if __name__ == '__main__':
    import time
    start = time.time()
    import os
    #p = 'C:\\Users\\wuyou\\Desktop\\UiTest\\logs\\tmp'
    p = 'C:\\cygwin64\\home\\c_youwu\\UiTest\\logs\\tmp'
    for f in os.listdir(p):
        ApplicationClassification.analysis_dump(os.path.join(p, f))
    print time.time()-start