__author__ = 'c_youwu'
from libs.GlobalVariable import GlobalVariable
from libs.Utility import Utility

package_name = "com.android.contacts"
Utility.stop_process_on_device(package_name)
Utility.stop_process_on_device('uiautomator')
Utility.push_file_to_device(local=GlobalVariable.uiautomator_jar, remote='/data/local/tmp/')
Utility.run_command_on_pc('adb root')
import os
abs_path = GlobalVariable.working_directory

thread = None
count = 0
log_path = Utility.make_dirs(os.path.join(GlobalVariable.logs_directory, package_name))
xml_store_path = Utility.make_dirs(os.path.join(log_path, 'xml'))




