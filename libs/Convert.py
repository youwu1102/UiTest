__author__ = 'c_youwu'
import os
from xml.dom.minidom import parse
from TraversalNode import TraversalNode
from xml.dom.minidom import Document

class Convert(object):
    def __init__(self):
        self.dict_traversal_node = dict()
        self.root = ''
        self.nodes = list()
        self.wuyou = []

    def Node2Action(self, path):
        self.__parse_config(path=path)

        if self.root:
            self.nodes.append((self.root, [], []))
            self.generate_test_case()
        else:
            print 'can not find root node ,break'

    def generate_test_case(self):
        while True:
            if self.nodes:
                    eigenvalue, E, A = self.nodes.pop()
                    node = self.dict_traversal_node.get(eigenvalue)
                    next_list = node.get_next()
                    optional_list = node.get_optional()
                    for e, a in next_list:
                        if e not in E:
                            # if optional_list:
                            #     for oa in optional_list:
                            #         nE = E[:]
                            #         nA = A[:]
                            #         if oa not in nA:
                            #             nA.append(oa)
                            #             nE.append(e)
                            #             nA.append(a)
                            #             self.nodes.append((e, nE, nA))
                            #             self.wuyou.append(nA)
                            # else:
                                nE = E[:]
                                nA = A[:]
                                nE.append(e)
                                nA.append(a)
                                self.nodes.append((e, nE, nA))
                                self.wuyou.append(nA)
                    # for n in next_list:
                    #     if n not in pre:
                    #         e, a = n
                    #         pre.append(n)
                    #         self.nodes.append((e, pre))
                    #         self.wuyou.append((eigenvalue, pre))
                    # for o in optional_list:
                    #     self.wuyou.append((eigenvalue, pre))
            else:
                break
        tmp ='C:\\1\\1'
        count = 0
        for wuyou in self.wuyou:
            count += 1
            self.write_test_case(actions=wuyou,save_path=os.path.join(tmp, '%s.xml' % count))

    def write_test_case(self, actions, save_path):
        doc = Document()
        root = doc.createElement('case')
        for action in actions:
            action_node = doc.createElement('action')
            action_node.setAttribute('name', 'click')
            if action.get('text'):
                action_node.setAttribute('text', action.get('text'))
            if action.get('content-desc'):
                action_node.setAttribute('desc', action.get('content-desc'))
            if action.get('resource-id'):
                action_node.setAttribute('id', action.get('resource-id'))
            if action.get('class'):
                action_node.setAttribute('class', action.get('class'))
            # if action.get('index'):
            #     action_node.setAttribute('index', action.get('index'))
            root.appendChild(action_node)
        doc.appendChild(root)
        f = open(save_path, 'w')
        f.write(doc.toprettyxml(indent='', encoding='utf-8'))
        f.close()

        # self.selector_mapping = {'text': 'text',
        #                          'id': 'resourceId',
        #                          'desc': 'description',
        #                          'class': 'className',
        #                          'index': 'index'}

    def __parse_config(self, path):
        dom = parse(path)
        root = dom.documentElement
        nodes = root.getElementsByTagName('Node')
        if True:
            for node in nodes:
                eigenvalue = node.getAttribute('eigenvalue')
                if node.getAttribute('root'):
                    self.root = eigenvalue
                traversal_node = TraversalNode(eigenvalue=eigenvalue)
                next_list = node.getElementsByTagName('Next')
                previous_list = node.getElementsByTagName('Previous')
                closed_list = node.getElementsByTagName('All')
                optional_list = node.getElementsByTagName('Optional')
                for next_node in next_list:
                    for info_node in next_node.getElementsByTagName('Info'):
                        tmp_e = info_node.getAttribute('eigenvalue')
                        tmp_a = info_node.getAttribute('action')
                        traversal_node.append_next((tmp_e, eval(tmp_a)))
                for previous_node in previous_list:
                    for info_node in previous_node.getElementsByTagName('Info'):
                        tmp_e = info_node.getAttribute('eigenvalue')
                        tmp_a = info_node.getAttribute('action')
                        traversal_node.append_previous((tmp_e, eval(tmp_a)))
                for optional_node in optional_list:
                    for info_node in optional_node.getElementsByTagName('Info'):
                        tmp_a = info_node.getAttribute('action')
                        traversal_node.append_optional(eval(tmp_a))
                for closed_node in closed_list:
                    for info_node in closed_node.getElementsByTagName('Info'):
                        tmp_a = info_node.getAttribute('action')
                        traversal_node.append_closed(eval(tmp_a))
                self.dict_traversal_node[eigenvalue] = traversal_node


if __name__ == '__main__':
    c =Convert()
    print os.path.exists('C:\\cygwin64\\home\\c_youwu\\UiTest\\repository\\CaseUtils\\SDM660\\com.android.mms\\Config.xml')
    c.Node2Action('C:\\cygwin64\\home\\c_youwu\\UiTest\\repository\\CaseUtils\\SDM660\\com.example.android.notepad\\Config.xml')