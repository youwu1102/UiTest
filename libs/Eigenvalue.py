# -*- encoding:UTF-8 -*-
import re
import difflib


class Eigenvalue(object):
    @staticmethod
    def calculate_eigenvalue(dump_xml):
        with open(dump_xml) as dump:
            dump_content = dump.read()
        pattern_class = re.compile(r'class=\".*?\"')
        pattern_resource_id = re.compile(r'resource-id=\".*?\"')
        pattern_text= re.compile(r'text=\".*?\"')
        Eigenvalue.__get_sequence(dump_content,pattern_class)
        print Eigenvalue.__get_kinds(dump_content, pattern_class)
        print Eigenvalue.__get_kinds(dump_content, pattern_resource_id)
        print Eigenvalue.__get_kinds(dump_content, pattern_text)

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


    @staticmethod
    def compare_dump(dump1, dump2):
        dump1_content=Eigenvalue.__open_dump(dump1)
        dump2_content=Eigenvalue.__open_dump(dump2)
        s = difflib.SequenceMatcher(None, dump1_content, dump2_content)
        for a in s.get_grouped_opcodes():
            print a
        # for tag, i1, i2, j1, j2 in s.get_opcodes():
        #     print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %  (tag, i1, i2, dump1_content[i1:i2], j1, j2, dump2_content[j1:j2]))

    @staticmethod
    def __open_dump(dump_path):
        with open(dump_path, 'r') as dump:
            tmp = dump.read()
        return tmp.replace('<node', '\n<node')


if __name__ == '__main__':
    import os
    p = "C:\\Users\\wuyou\\Desktop\\UiTest\\logs\\tmp"
    d1= os.path.join(p,'dump_1035839587978767125.uix')
    d2= os.path.join(p,'dump_5694674565452784425.uix')
    Eigenvalue.compare_dump(d1,d2)