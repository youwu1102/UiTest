__author__ = 'c_youwu'
from Utility import Utility
from Eigenvalue import Eigenvalue


class ApplicationClassification(object):

    dict_high_priority = dict()
    dict_blacklist = dict()
    dict_dump_actions = dict()
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
        if eigenvalue not in ApplicationClassification.dict_dump_actions.keys():
            ApplicationClassification.dict_dump_actions[eigenvalue]=dump_xml
            print 'new : '+ ApplicationClassification.dict_dump_actions.get(eigenvalue)
        else:

            print dump_xml
            print 'is same as:'+ ApplicationClassification.dict_dump_actions.get(eigenvalue)
            print '==========================================================='

if __name__ == '__main__':
    import time
    start = time.time()
    import os
    p = 'C:\\Users\\wuyou\\Desktop\\UiTest\\logs\\tmp'
    # p = 'C:\\cygwin64\\home\\c_youwu\\UiTest\\logs\\tmp'
    for f in os.listdir(p):
        ApplicationClassification.analysis_dump(os.path.join(p, f))
    print time.time()-start