__author__ = 'c_youwu'
from GlobalVariable import GlobalVariable


class TraversalNode(object):
    def __init__(self, eigenvalue):
        self.__eigenvalue = eigenvalue
        self.__total = list()
        self.__closed = list()
        self.__attempts = 0
        self.__type = 'normal'
        self.__id = -1

    def init_total(self, window_nodes):
        self.__total = window_nodes[:]
        self.__set_type()

    def add_to_closed(self, element):
        self.__closed.append(element)

    def __set_type(self):
        for member in self.__total:
            if member.get('package') != GlobalVariable.package_name:
                self.__type = 'illegal'
                break

    def merge_total(self, window_nodes):
        for window_node in window_nodes:
            if window_node not in self.__total:
                self.__total.append(window_node)

    def get_total(self):
        return self.__total

    def get_open(self):
        __open = list()
        for x in self.__total:
            if x not in self.__closed:
                __open.append(x)
        return __open

    def get_closed(self):
        return self.__closed

    def get_eigenvalue(self):
        return self.__eigenvalue

    def add_attempts(self):
        self.__attempts += 1
        return self.__attempts

    def reset_attempts(self):
        self.__attempts = 0
        return self.__attempts

    def get_attempts(self):
        return self.__attempts

    def set_id(self, id):
        if self.__id == -1:
            self.__id = id
        return self.__id

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__type