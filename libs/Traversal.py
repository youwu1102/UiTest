__author__ = 'c_youwu'



class TraversalNode(object):
    def __init__(self,eigenvalue):
        self.__eigenvalue = eigenvalue
        self.__open = []
        self.__closed = []
        self.__previous = []
        self.__next = []

    def append_previous(self):
        pass

    def append_next(self):
        pass

    def init_open(self):
        pass

    def move_to_closed(self, element):
        pass

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