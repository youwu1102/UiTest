__author__ = 'c_youwu'
from libs.Utility import Utility
from libs.GlobalVariable import GlobalVariable
from libs.ApplicationClassification import ApplicationClassification
package_name = "com.android.contacts"
Utility.stop_process_on_device(package_name)
Utility.stop_process_on_device('uiautomator')
Utility.push_file_to_device(local=GlobalVariable.uiautomator_jar, remote='/data/local/tmp/')
Utility.run_command_on_pc('adb root')
import time
import os
from subprocess import Popen
from subprocess import PIPE
abs_path = GlobalVariable.working_directory
a = Popen('adb shell uiautomator runtest /data/local/tmp/Demo.jar -c Monday.afternoon#test3rd_App', stdout=PIPE, stderr=PIPE, shell=True)
Utility.run_command_on_device('am start %s' % package_name)
thread = None
count = 0
for line in iter(a.stdout.readline, ''):
    if 'STATE:WAIT' in line:
        count += 1
        if not thread or not thread.is_alive():
            thread = ApplicationClassification()
            thread.start()
        print time.time()

        # tmp_xml = os.path.join(abs_path, 'logs', 'tmp', '%s.xml' % count)
        # tmp_txt = os.path.join(abs_path, 'logs', 'tmp', '%s.txt' % count)
        # os.system('adb pull /data/local/tmp/current.xml %s' % tmp_xml)
        # ApplicationClassification.analysis_dump(tmp_xml)
        #os.system('adb push C:\Users\c_youwu\Desktop\UiTest\\tmp\\tmp.txt /data/local/tmp/Action.txt')
        #os.system('adb push %s /data/local/tmp/Action.txt' % tmp_txt)
    elif 'STATE:' in line:
        print line
    # elif 'STATE:UiObjectNotFoundException' in line:
    #     print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
    # else:
    #     pass
    # if count % 10 ==0:
    #     pass

