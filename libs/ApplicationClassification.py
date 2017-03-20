__author__ = 'c_youwu'
from Utility import Utility
from Eigenvalue import Eigenvalue

class ApplicationClassification(object):

    dict_high_priority = dict()
    dict_blacklist = dict()
    list_attrs = ['index', 'text', 'resource-id', 'package', 'content-desc', 'checkable', 'checked',
                  'clickable', 'enabled', 'focusable', 'focused', 'scrollable', 'long-clickable',
                  'password', 'selected', 'bounds', 'class']

    @staticmethod
    def write_action_file():
        pass

    @staticmethod
    def analysis_dump(dump_xml):
        dump_content = Utility.open_dump(dump_xml)
        eigenvalue = Eigenvalue.calculate_eigenvalue(dump_content)

        print dump_xml

if __name__ == '__main__':
    import time
    start = time.time()
    import os
    p = 'C:\\cygwin64\\home\\c_youwu\\UiTest\\logs\\tmp'
    for f in os.listdir(p):
        print ApplicationClassification.analysis_dump(os.path.join(p, f))
    print time.time()-start