# -*- encoding:UTF-8 -*-
__author__ = 'c_youwu'
import re


class Utility(object):

    @staticmethod
    def calculate_eigenvalue(dump_xml):
        with open(dump_xml) as dump:
            dump_content = dump.read()
        pattern_class = re.compile(r'class=\".*?\"')
        pattern_resource_id = re.compile(r'resource-id=\".*?\"')
        pattern_text= re.compile(r'text=\".*?\"')
        Utility.__get_sequence(dump_content,pattern_class)
        print Utility.__get_kinds(dump_content, pattern_class)
        print Utility.__get_kinds(dump_content, pattern_resource_id)
        print Utility.__get_kinds(dump_content, pattern_text)


    @staticmethod
    def __get_kinds(content, pattern):
        list_type = []
        results = pattern.findall(content)
        for result in results:
            if result not in list_type:
                list_type.append(result)
        return len(list_type)

    @staticmethod
    def __get_sequence(content, pattern):
        string = ''
        for re_result in pattern.finditer(content):
            print re_result.group()
        return string







if __name__ == '__main__':
    import os
    p="C:\\Users\\c_youwu\Desktop\\traing\\"
    for x in os.listdir(p):
        if x.endswith('.uix'):
            print x
            Utility.calculate_eigenvalue(os.path.join(p,x))

