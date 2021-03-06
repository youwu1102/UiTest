# -*- encoding:UTF-8 -*-
from PrintInfo import Print
from GlobalVariable import GlobalVariable
import os
import re
from time import sleep
from ADB import Adb
from TimeFormat import TimeFormat
import random
import string

class Utility(object):
    pid_expression = re.compile(r'\d{4,5} ')

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
    def stop_process_on_device(process_name):
        result = Utility.run_command_on_device(cmd='ps | grep %s | grep -v grep' % process_name, need_output=True)
        for line in result.split('\n'):
                if line:
                    for re_result in Utility.pid_expression.finditer(line):
                        pid = re_result.group()
                        Utility.run_command_on_device(cmd='kill %s' % pid)
                        break
                    Utility.wait_for_time(1)

    @staticmethod
    def start_process_on_device(package, activity=''):
        Print.info('I want to start the process \"%s\"' % package)
        if activity:
            Utility.run_command_on_device(cmd='am start -n %s/%s' % (package, activity))
        else:
            Utility.run_command_on_device(cmd='am start %s' % package)
        Utility.wait_for_time(5)

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
    def random_char(length):
        return ''.join(random.choice(string.letters) for x in range(length))

    @staticmethod
    def random_number():
        return str(random.randint(1, 99999999))


if __name__ == '__main__':
    print Utility.random_char(10)

