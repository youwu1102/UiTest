# -*- encoding:UTF-8 -*-
import re
from xml.etree.ElementTree import ElementTree, Element
from GlobalVariable import GlobalVariable


class Eigenvalue(object):
    dict_class_name_mapping_id = dict()

    @staticmethod
    def __get_dict_of_class_name_mapping_id(xml_path):
        tmp_dict = dict()
        tree = ElementTree()
        tree.parse(xml_path)
        nodes = tree.findall('class')
        for node in nodes:
            tmp_dict[node.get('name')] = node.get('id')
        return tmp_dict

    @staticmethod
    def insert_class_name_mapping_in_xml(xml_path, class_name, class_id):
        tree = ElementTree()
        tree.parse(xml_path)
        root = tree.getroot()
        element = Element('class', {'name': class_name, 'id': '%s' % class_id})
        element.tail = '\n\t'
        root.append(element)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def calculate_eigenvalue(dump_content):
        return Eigenvalue.__get_class_name_sequence(dump_content)

    @staticmethod
    def __get_kinds(content, pattern):
        list_type = []
        results = pattern.findall(content)
        for result in results:
            if result not in list_type:
                list_type.append(result)
        return len(list_type)

    @staticmethod
    def __get_class_name_sequence(content):
        pattern = re.compile(r'class=\".*?\"')
        if not Eigenvalue.dict_class_name_mapping_id:
            Eigenvalue.dict_class_name_mapping_id = Eigenvalue.__get_dict_of_class_name_mapping_id(
                GlobalVariable.class_name_mapping_id_configuration)
        sequence = ''
        for re_result in pattern.finditer(content):
            class_name = re_result.group().replace('class="', '')[:-1]
            sequence += Eigenvalue.__get_id_of_class_name(class_name=class_name)
        if len(sequence) > 60:
            return sequence[:60]
        return sequence

    @staticmethod
    def __get_id_of_class_name(class_name):
        class_id = Eigenvalue.dict_class_name_mapping_id.get(class_name)
        if not class_id:
            class_id = len(Eigenvalue.dict_class_name_mapping_id)
            Eigenvalue.insert_class_name_mapping_in_xml(GlobalVariable.class_name_mapping_id_configuration, class_name, class_id)
            Eigenvalue.dict_class_name_mapping_id = Eigenvalue.__get_dict_of_class_name_mapping_id(
                GlobalVariable.class_name_mapping_id_configuration)
        return '%03x' % int(class_id)

if __name__ == '__main__':
    pass
    # import time
    # start = time.time()
    # import os
    # p = 'C:\\cygwin64\\home\\c_youwu\\UiTest\\logs\\tmp'
    # for f in os.listdir(p):
    #     print Eigenvalue.calculate_eigenvalue(os.path.join(p, f))
    # print time.time()-start
    # dict_class_name_mapping = Eigenvalue.get_dict_of_class_name_mapping(GlobalVariable.class_name_mapping_id_configuration)
    # if class_name not in dict_class_name_mapping.keys():
    #     Eigenvalue.insert_class_name_mapping_in_xml(GlobalVariable.class_name_mapping_id_configuration, class_name, len(dict_class_name_mapping.keys()))
    # import os
    # p = "C:\\Users\\wuyou\\Desktop\\UiTest\\logs\\tmp"
    # d1= os.path.join(p,'dump_1035839587978767125.uix')
    # d2= os.path.join(p,'dump_5694674565452784425.uix')
    # Eigenvalue.compare_dump(d1,d2)