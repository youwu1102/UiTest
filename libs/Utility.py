# -*- encoding:UTF-8 -*-
from PrintInfo import Print
from GlobalVariable import GlobalVariable
import os
import re
from time import sleep
from ADB import Adb
from Eigenvalue import Eigenvalue
from xml.dom import minidom
from DumpNodes import DumpNodes
from TimeFormat import TimeFormat
from TraversalNode import TraversalNode


class Utility(object):
    pid_expression = re.compile(r'\d{3,5} ')

    @staticmethod
    def run_command_on_pc(cmd, except_result='', except_true=True, need_output=False):
        """
        这个方法只是在本机上运行，只有pc模式下用到 或者部分SSH
        cmd 需要执行的命令  必填项
        action_info 操作说明，非空则打印具体的操作，非必填项
        except_result 期望出现的字符串，非空则去执行判断，与except_true相互配合 ，非必填项
        except_true except_result，默认为True，如果修改成False的话，意思相当于不期望出现的字符串
        举例 run_command_on_device('ps | grep python', action_info='', except_result='python', except_true=False)
        代表在手机中执行了  ps | grep python  命令
        如果结果中包含Python 字样  则返回 False
        即可以理解为 希望结果中不出现Python字样
        """
        Print.info('I run the command: %s' % cmd)
        actual_result = os.popen(cmd).read().strip('\r\n')
        if need_output and not except_result:
            Print.info('I get the command output: %s' % actual_result)
            return actual_result
        if except_result:
            return Utility.check_result(except_result=except_result, except_true=except_true, actual_result=actual_result)
        return True

    @staticmethod
    def run_command_on_device(cmd, except_result='', except_true=True, need_output=False):
        """
        方法根据3种execution_mode ：ssh , pc, device 来控制操作的方法
        总共传递4个参数
        cmd 需要执行的命令  必填项
        action_info 操作说明，非空则打印具体的操作，非必填项
        except_result 期望出现的字符串，非空则去执行判断，与except_true相互配合 ，非必填项
        except_true except_result，默认为True，如果修改成False的话，意思相当于不期望出现的字符串
        举例 run_command_on_device('ps | grep python', action_info='', except_result='python', except_true=False)
        代表在手机中执行了  ps | grep python  命令
        如果结果中包含Python 字样  则返回 False
        即可以理解为 希望结果中不出现Python字样
        """
        cmd = '%s shell \"%s\"' % (GlobalVariable.adb_exe, cmd)
        Print.info('I run the command: %s' % cmd)
        actual_result = os.popen(cmd).read().strip('\r\n')
        if need_output and not except_result:
            Print.info('I get the command output: %s' % actual_result)
            return actual_result
        if except_result:
            return Utility.check_result(except_result=except_result, except_true=except_true, actual_result=actual_result)
        return True

    @staticmethod
    def check_result(except_result, except_true, actual_result):

        """
        参考上方 run_command_on_device 中描述
        """
        if except_true:
            if except_result in actual_result:
                Print.info('I except:\"%s\"' % except_result + ' in command output:\"%s\"' % actual_result)
                return True
            else:
                Print.error('I except:\"%s\"' % except_result + ' in command output:\"%s\"' % actual_result)
                return False
        else:
            if except_result in actual_result:
                Print.error('I do not except:\"%s\"' % except_result + ' in command output:\"%s\"' % actual_result)
                return False
            else:
                Print.info('I do not except:\"%s\"' % except_result + ' in command output:\"%s\"' % actual_result)
                return True

    @staticmethod
    def stop_process_on_device(process_name, not_matching=''):
        Print.info('I want to terminate the process \"%s\"' % process_name)
        pids = Utility.get_process_id_on_device(process_name=process_name, not_matching=not_matching)
        for pid in pids:
            Utility.run_command_on_device(cmd='kill %s' % pid[:-1])

    @staticmethod
    def start_process_on_device(process_name):
        Print.info('I want to start the process \"%s\"' % process_name)
        Utility.run_command_on_device(cmd='am start %s' % process_name)

    @staticmethod
    def get_process_id_on_device(process_name, not_matching=''):
        pids = []
        if not_matching:
            result = Utility.run_command_on_device(
                cmd='ps | grep %s | grep -v grep |grep -v %s' % (process_name, not_matching), need_output=True)
            for line in result.split('\r\n'):
                for re_result in Utility.pid_expression.finditer(line):
                    pids.append(re_result.group())
                    break
        else:
            result = Utility.run_command_on_device(cmd='ps | grep %s | grep -v grep' % process_name, need_output=True)
            for line in result.split('\r\n'):
                for re_result in Utility.pid_expression.finditer(line):
                    pids.append(re_result.group())
                    break
        return pids

    @staticmethod
    def push_file_to_device(local, remote, serial_number=''):
        cmd = Adb.push(local=local, remote=remote, serial_number=serial_number)
        Utility.run_command_on_pc(cmd)
        sleep(1)

    @staticmethod
    def pull_file_to_pc(remote, local, serial_number=''):
        cmd = Adb.pull(remote=remote, local=local, serial_number=serial_number)
        Utility.run_command_on_pc(cmd)
        sleep(1)

    @staticmethod
    def open_dump(dump_path):
        with open(dump_path, 'r') as dump:
            content = dump.read()
        return content

    @staticmethod
    def make_dirs(path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def output_msg(msg, level='i'):
        level = level.lower()
        if level == 'i':
            Print.info(msg)
        elif level == 'e':
            Print.error(msg)
        elif level == 'r':
            Print.result(msg)
        elif level == 'w':
            Print.warm(msg)
        else:
            Print.debug(msg)


    @staticmethod
    def analysis_dump(dump_path):
        Utility.output_msg('I will analysis the dump file: %s' % dump_path)
        eigenvalue = Eigenvalue.calculate_eigenvalue(dump_path)
        Utility.output_msg('I get the eigenvalue: %s ' % eigenvalue)
        if eigenvalue not in GlobalVariable.dict_E_M_N.keys():
            Utility.output_msg('This eigenvalue has not appeared before.')
            node = TraversalNode(eigenvalue)
            node.append_previous()
            node.init_open(Utility.__get_actions_from_dump(dump_path))
            GlobalVariable.dict_E_M_N[eigenvalue] = node
        else:
            Utility.output_msg('This eigenvalue has appeared before.')
        return eigenvalue

    @staticmethod
    def __get_actions_from_dump(dump_path):
        nodes = Utility.__get_nodes_from_dump(dump_path)
        actions = Utility.__category_nodes(nodes)
        return actions

    @staticmethod
    def calculate_eigenvalue(dump_path):
        eigenvalue = Eigenvalue.calculate_eigenvalue(dump_path=dump_path)
        Utility.output_msg('Tbe current dump eigenvalue is:%s' % eigenvalue)
        return eigenvalue

    @staticmethod
    def __get_nodes_from_dump(dump_path):
        node_list = []
        dom = minidom.parse(dump_path)
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        for node in nodes:
            dict_node = {}
            for attr in GlobalVariable.list_attrs:
                dict_node[attr] = node.getAttribute(attr)
            node_list.append(dict_node)
        return node_list

    @staticmethod
    def __category_nodes(dump_nodes):  # 分类节点，将有用的留下 删除没用的
        DumpNodes.remove_useless_nodes(dump_nodes)
        return dump_nodes

    @staticmethod
    def get_timestamp():
        return TimeFormat.timestamp()

    @staticmethod
    def wait_for_time(seconds):
        Print.info('I wait for %s seconds' % seconds)
        sleep(seconds)

    @staticmethod
    def restart_process_on_devices(package_name):
        Utility.stop_process_on_device(package_name)
        Utility.wait_for_time(1)
        Utility.start_process_on_device(package_name)
        Utility.wait_for_time(1)

    @staticmethod
    def get_selector(action):
        dict_tmp = dict()
        for key in GlobalVariable.dict_selector.keys():
            key_value = action.get(key)
            if key_value:
                dict_tmp[GlobalVariable.dict_selector.get(key)] = key_value
        return dict_tmp

if __name__ == '__main__':
    for x in range(10000):
        aaa = Utility.analysis_dump('C:\\cygwin64\\home\\c_youwu\\UiTest\\logs\\2017_03_27-16_31_38\\com.android.contacts\\2.uix')

