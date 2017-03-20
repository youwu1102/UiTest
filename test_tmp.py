__author__ = 'c_youwu'
from libs.Utility import Utility
from libs.GlobalVariable import GlobalVariable


Utility.stop_process_on_device('uiautomator')
Utility.push_file_to_device(local=GlobalVariable.uiautomator_jar, remote='/data/local/tmp/')
Utility.run_command_on_pc('adb root')

import os
from subprocess import Popen
from subprocess import PIPE
#Utility.run_command_on_device('uiautomator runtest Demo.jar -c Monday.afternoon#test3rd_App')
a = Popen('adb shell uiautomator runtest /data/local/tmp/Demo.jar -c Monday.afternoon#test3rd_App', stdout=PIPE, stderr=PIPE, shell=True)
count = 0
abs_path = GlobalVariable.working_directory
package_name = "com.android.contacts"



for line in iter(a.stdout.readline, ''):
    print line
    if 'STATE:WAIT' in line:
        count += 1
        tmp_xml = os.path.join(abs_path, 'logs', 'tmp', '%s.xml' % count)
        tmp_txt = os.path.join(abs_path, 'logs', 'tmp', '%s.txt' % count)
        os.system('adb pull /data/local/tmp/current.xml %s' % tmp_xml)
        #os.system('adb push C:\Users\c_youwu\Desktop\UiTest\\tmp\\tmp.txt /data/local/tmp/Action.txt')
        #os.system('adb push %s /data/local/tmp/Action.txt' % tmp_txt)
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
