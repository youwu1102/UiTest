__author__ = 'c_youwu'
from GlobalVariable import GlobalVariable

class TraversalNode(object):
    def __init__(self, eigenvalue):
        self.__eigenvalue = eigenvalue
        self.__open = []
        self.__closed = []
        self.__previous = []
        self.__next = []

    def append_previous(self):
        if GlobalVariable.previous_node and GlobalVariable.previous_step:
            self.__previous.append([GlobalVariable.previous_node, GlobalVariable.previous_step])
        else:
            print('Can not find previous node.')

    def append_next(self):
        pass

    def init_open(self, window_nodes):
        self.__open = window_nodes

    def move_to_closed(self, element):
        print self.__closed
        self.__open.remove(element)
        self.__closed.append(element)
        print self.__closed


    def get_open(self):
        return self.__open

    def get_closed(self):
        return self.__closed

    def get_node_eigenvalue(self):
        return self.__eigenvalue

    def get_previous(self):
        return self.__previous

    def get_next(self):
        return self.__next