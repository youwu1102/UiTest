__author__ = 'c_youwu'
import os
import sys
import time
abs_path = sys.argv[0].replace('/test.py','')
from libs.Analysis import Analysis
import traceback
dict_ui_test = dict()

def get_md5_windows(file_path):
    string = os.popen('certutil -hashfile %s MD5' % file_path).readlines()
    return string[1].replace(' ','').strip('\r\n')

def get_list(tmp_xml):
        try:
            return Analysis.ui_dump(tmp_xml, 'Forum').get('Action')
        except Exception,e:
            print traceback.format_exc()
            os.system('adb pull /data/local/tmp/current.xml %s' % tmp_xml)
            return get_list(tmp_xml)
from subprocess import Popen
from subprocess import PIPE
a = Popen('adb shell uiautomator runtest /data/local/tmp/Demo.jar -c Monday.afternoon#test3rd_App', stdout=PIPE, stderr=PIPE, shell=True)
count = 0
for line in iter(a.stdout.readline, ''):
    if 'STATE:WAIT' in line:
        count += 1
        tmp_xml = os.path.join(abs_path, 'logs', 'tmp', '%s.xml' % count)
        tmp_txt = os.path.join(abs_path, 'logs', 'tmp', '%s.txt' % count)
        os.system('adb pull /data/local/tmp/current.xml %s' % tmp_xml)
        os.system('adb push C:\\Git\\UiTest\\tmp\\blank.txt /data/local/tmp/Action.txt')
        md5 = get_md5_windows(tmp_xml)
        if md5 not in dict_ui_test.keys():
            dict_ui_test[md5] = get_list(tmp_xml)

        list_actions = dict_ui_test.get(md5)
        if len(list_actions) > 0:
            actions = list_actions[0]
            del list_actions[0]
            w_file = open(tmp_txt, 'w')
            for action in actions:
                print action.encode('utf-8')
                w_file.write(action.encode('utf-8') + '\n')
            w_file.close()
        else:
            action = '%04d,\t' % (6+len('BACK')) + 'BACK' +'\n'
            w_file = open(tmp_txt, 'w')
            w_file.write(action)
            w_file.close()
        os.system('adb push %s /data/local/tmp/Action.txt' % tmp_txt)
    elif 'STATE:DumpException' in line:
        print '**************************************'
        print '**************************************'
        print '**************************************'
        print '**************************************'
        print '**************************************'

    elif 'STATE:UiObjectNotFoundException' in line:
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
    else:
        print line

a.kill()


# for x in xrange(10000):
#     tmp_xml = os.path.join(abs_path, 'logs', 'tmp', '%s.xml' % x)
#     tmp_txt = os.path.join(abs_path, 'logs', 'tmp', '%s.txt' % x)
#     os.system('adb pull /data/local/tmp/current.xml %s' % tmp_xml)
#     md5 = get_md5_windows(tmp_xml)
#
#     if md5 not in dict_ui_test.keys():
#         dict_ui_test[md5] = get_list(tmp_xml)
#
#     list_actions = dict_ui_test.get(md5)
#     if len(list_actions) > 0:
#         actions = list_actions[0]
#         del list_actions[0]
#         w_file = open(tmp_txt, 'w')
#         for action in actions:
#             print action.encode('utf-8')
#             w_file.write(action.encode('utf-8') + '\n')
#         w_file.close()
#     else:
#         action = '%04d,\t' % (6+len('BACK')) + 'BACK' +'\n'
#         w_file = open(tmp_txt, 'w')
#         w_file.write(action)
#         w_file.close()
#
#     os.system('adb push %s /data/local/tmp/Action.txt' % tmp_txt)
#     print x
#     time.sleep(1)


