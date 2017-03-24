# -*- encoding:UTF-8 -*-
from os.path import join


class GlobalVariable(object):

    working_directory = 'C:\\cygwin64\\home\\c_youwu\\UiTest'
    # working_directory = 'C:\\Users\\wuyou\\Desktop\\UiTest'

    configs_directory = join(working_directory, 'configs')
    logs_directory = join(working_directory, 'logs')
    host_utils = join(working_directory, 'repository', 'HostUtils')
    target_utils = join(working_directory, 'repository', 'TargetUtils')

    adb_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    aapt_exe = join(host_utils, 'sdk_tools', 'adb.exe')
    fastboot_exe = join(host_utils, 'sdk_tools', 'fastboot.exe')

    blank_action_file = join(target_utils, 'blank.txt')

    class_name_mapping_id_configuration = join(configs_directory, 'class_name_mapping_id', 'config.xml')

    uiautomator_jar = 'C:\\cygwin64\\home\\c_youwu\\UiTest\\repository\\UiAutomatorCode\\UiTest\\bin\\Demo.jar'

    list_attrs = ['index', 'text', 'resource-id', 'package', 'content-desc', 'checkable', 'checked',
                  'clickable', 'enabled', 'focusable', 'focused', 'scrollable', 'long-clickable',
                  'password', 'selected', 'bounds', 'class']

    # ===============================================

    dict_dump_actions = dict()

if __name__ == '__main__':
    print GlobalVariable.host_utils