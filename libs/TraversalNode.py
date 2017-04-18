__author__ = 'c_youwu'
from Utility import Utility

class TraversalNode(object):
    def __init__(self, eigenvalue):
        self.__eigenvalue = eigenvalue
        self.__open = []
        self.__closed = []
        self.__previous = []
        self.__next = []

    def append_previous(self, previous):
        if previous:
            Utility.output_msg('\"%s\" node will append %s as previous.' % (self.__eigenvalue, str(previous)))
            self.__previous.append(previous)
        else:
            Utility.output_msg('Previous is None', 'e')

    def append_next(self, next):
        if next:
            Utility.output_msg('\"%s\" node will append %s as next.' % (self.get_node_eigenvalue(), str(next)))
            self.__next.append(next)
        else:
            Utility.output_msg('Next is None', 'e')

    def init_open(self, window_nodes):
        self.__open = window_nodes

    def move_to_closed(self, element):
        self.__open.remove(element)
        self.__closed.append(element)

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