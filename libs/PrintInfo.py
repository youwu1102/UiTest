# -*- encoding:UTF-8 -*-
from TimeFormat import TimeFormat
import traceback


class Print(object):
    LogPath = 'UiTest.log'

    @staticmethod
    def info(msg):
        msg = TimeFormat.timestamp() + '  INFO: ' + str(msg)
        print msg
        Print.__write(msg)

    @staticmethod
    def warm(msg):
        msg = TimeFormat.timestamp() + '  WARM: ' + str(msg)
        print msg
        Print.__write(msg)

    @staticmethod
    def error(msg):
        msg = TimeFormat.timestamp() + ' ERROR: ' + str(msg)
        print msg
        Print.__write(msg)

    @staticmethod
    def debug(msg):
        msg = TimeFormat.timestamp() + ' DEBUG: ' + str(msg)
        #print msg
        Print.__write(msg)

    @staticmethod
    def result(msg):
        msg = TimeFormat.timestamp() + '  RSLT: ' + str(msg)
        print msg
        Print.__write(msg)

    @staticmethod
    def __write(msg):
        log = open(Print.LogPath, 'a+', 1)
        msg = msg.strip('\r\n')+'\n'
        log.write(msg)
        log.close()

    @staticmethod
    def traceback():
        tmp = traceback.format_exc()
        if tmp != 'None\n':
            Print.debug(tmp.strip('\n'))







