# -*- encoding:UTF-8 -*-
from os.path import join

class GlobalVariable(object):
    # working_directory = 'C:\\cygwin64\\home\\c_youwu\\UiTest'
    working_directory = 'C:\\Users\\wuyou\\Desktop\\UiTest'

    configs_directory = join(working_directory, 'configs')
    logs_directory = join(working_directory, 'logs')
    host_utils = join(working_directory, 'repository', 'HostUtils')
    target_utils = join(working_directory, 'repository', 'TargetUtils')
    case_utils = join(working_directory, 'repository', 'CaseUtils')

    current_case_directory = ''
    current_log_directory = ''

    adb_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    aapt_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    fastboot_exe = join(host_utils, 'sdk_tools', 'fastboot.exe')

    class_name_mapping_configuration = join(configs_directory, 'class_name_mapping_id', 'config.xml')
    list_attrs = ['index', 'text', 'resource-id', 'package', 'content-desc', 'checkable', 'checked',
                  'clickable', 'enabled', 'focusable', 'focused', 'scrollable', 'long-clickable',
                  'password', 'selected', 'bounds', 'class']
    dict_selector = {'index': 'index',
                     'text': 'text',
                     'resource-id': 'resourceId',
                     'content-desc': 'description',
                     'class': 'className'}

    # ===============================================

    dict_E_M_N = dict()  # eigenvalue mapping node


if __name__ == '__main__':
    print GlobalVariable.host_utils