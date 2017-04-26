__author__ = 'c_youwu'
from Utility import Utility

class TraversalNode(object):
    def __init__(self, eigenvalue):
        self.__eigenvalue = eigenvalue
        self.__optional = []
        self.__open = []
        self.__closed = []
        self.__previous = []
        self.__next = []

    def append_previous(self, _previous):
        if _previous:
            Utility.output_msg('\"%s\" node will append %s as previous.' % (self.__eigenvalue, str(_previous)))
            self.__previous.append(_previous)
        else:
            Utility.output_msg('Previous is None', 'e')

    def append_next(self, _next):
        if _next:
            Utility.output_msg('\"%s\" node will append %s as next.' % (self.__eigenvalue, str(_next)))
            self.__next.append(_next)
        else:
            Utility.output_msg('Next is None', 'e')

    def append_closed(self, _closed):
        if _closed:
            Utility.output_msg('\"%s\" node will append %s as closed.' % (self.__eigenvalue, str(_closed)))
            self.__closed.append(_closed)
        else:
            Utility.output_msg('Closed is None', 'e')

    def append_optional(self, _optional):
        if _optional:
            Utility.output_msg('\"%s\" node will append %s as optional.' % (self.__eigenvalue, str(_optional)))
            self.__optional.append(_optional)
        else:
            Utility.output_msg('Optional is None', 'e')

    def init_open(self, window_nodes):
        if not window_nodes and self.__open:
            self.__closed = self.__open[:]
        else:
            for window_node in window_nodes:
                if window_node.get('action') == 'Click':
                    self.__open.append(window_node)
                elif window_node.get('action') == 'Edit':
                    self.__optional.append(window_node)

    def move_to_optional(self, element):
        self.__open.remove(element)
        self.__optional.append(element)

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

    def get_optional(self):
        return self.__optional