# -*- encoding:UTF-8 -*-
__author__ = 'wuyou'
import time

class TimeFormat(object):
    __FORMAT = '%Y_%m_%d-%H_%M_%S'

    @staticmethod
    def set_time_format(time_format):
        TimeFormat.__FORMAT = time_format

    @staticmethod
    def get_time_format():
        return TimeFormat.__FORMAT

    @staticmethod
    def timestamp():
        return time.strftime(TimeFormat.__FORMAT, time.localtime(time.time()))

if __name__ == '__main__':
    TimeFormat.set_time_format('%m-%d =%H:%M:%S')
    for x in range(10):
        TimeFormat.set_time_format('%m-%d =%H:%M:%S'+str(x))
        print TimeFormat.timestamp()
    print TimeFormat().get_time_format()