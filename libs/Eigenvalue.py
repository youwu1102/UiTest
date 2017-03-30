# -*- encoding:UTF-8 -*-
import re
from xml.etree.ElementTree import ElementTree, Element
from GlobalVariable import GlobalVariable
import xml.dom.minidom as xdm
from xml.dom.minidom import Node
class Eigenvalue(object):
    @staticmethod
    def __get_dict_of_number_map_letter(upper=True):
        count = 0
        dict_tmp = dict()
        letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if not upper:
            letter = letter.lower()
        for s in letter:
            dict_tmp[count] = s
            count += 1
        return dict_tmp

    @staticmethod
    def __get_dict_of_letter_map_number(upper=True):
        count = 0
        dict_tmp = dict()
        letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if not upper:
            letter = letter.lower()
        for s in letter:
            dict_tmp[s] = count
            count += 1
        return dict_tmp

    @staticmethod
    def __get_dict_of_class_name_mapping(config_path):
        tmp_dict = dict()
        tree = ElementTree()
        tree.parse(config_path)
        nodes = tree.findall('class')
        for node in nodes:
            tmp_dict[node.get('name')] = (node.get('id'), node.get('type'))
        return tmp_dict
    dict_number_letter = __get_dict_of_number_map_letter.__func__(upper=False)
    dict_letter_map_number = __get_dict_of_letter_map_number.__func__(upper=False)
    dict_class_name_mapping = __get_dict_of_class_name_mapping.__func__(config_path=GlobalVariable.class_name_mapping_configuration)

    #dict_number_map_lower_letter = __get_dict_of_number_map_letter.__func__(upper=False)
    #dict_upper_letter_map_number = __get_dict_of_letter_map_number.__func__(upper=True)

    @staticmethod
    def convert_26_to_10(x):
        x = x.upper()
        x1 = Eigenvalue.dict_letter_map_number.get(x[0])
        x2 = Eigenvalue.dict_letter_map_number.get(x[1])
        return x1 * 26 + x2

    @staticmethod
    def convert_10_to_26(x):
        x = int(x)
        x1 = x / 26
        x2 = x % 26
        return Eigenvalue.dict_number_letter.get(x1) + Eigenvalue.dict_number_letter.get(x2)

    @staticmethod
    def insert_class_name_mapping_in_xml(xml_path, class_name, class_id):
        tree = ElementTree()
        tree.parse(xml_path)
        root = tree.getroot()
        element = Element('class', {'name': class_name, 'id': class_id, 'type': 'common'})
        element.tail = '\n\t'
        root.append(element)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def calculate_eigenvalue(dump_path):
        return Eigenvalue.__get_class_name_sequence(dump_path)

    @staticmethod
    def __get_kinds(content, pattern):
        list_type = []
        results = pattern.findall(content)
        for result in results:
            if result not in list_type:
                list_type.append(result)
        return len(list_type)

    @staticmethod
    def __get_class_name_sequence(dump_path):
        dom = xdm.parse(dump_path)
        root = dom.documentElement
        sequence = Eigenvalue.__get_child(parent=root)
        return sequence[1:-1]

    @staticmethod
    def __get_child(parent):
        if parent.nodeType != Node.TEXT_NODE:
            sequence = '<'
            class_name = parent.getAttribute("class")
            if class_name:
                sequence += Eigenvalue.__convert_class_name_to_id(class_name)
            children = parent.childNodes
            for child in children:
                sequence += Eigenvalue.__get_child(child)
            return sequence + '>'
        return ''

    @staticmethod
    def __convert_class_name_to_id(class_name):
        if class_name not in Eigenvalue.dict_class_name_mapping.keys():
            class_id = len(Eigenvalue.dict_class_name_mapping)
            Eigenvalue.insert_class_name_mapping_in_xml(GlobalVariable.class_name_mapping_configuration,
                                                        class_name,
                                                        str(class_id))
            Eigenvalue.dict_class_name_mapping = Eigenvalue.__get_dict_of_class_name_mapping(
                GlobalVariable.class_name_mapping_configuration)
        class_id, class_type = Eigenvalue.dict_class_name_mapping.get(class_name)
        return Eigenvalue.__convert_to_letter(class_id, class_type)

    @staticmethod
    def __convert_to_letter(class_id, class_type):
        class_id = Eigenvalue.convert_10_to_26(class_id)
        if class_type == 'common':
            return class_id
        elif class_type == 'list':
            return class_id.upper()

if __name__ == '__main__':
    print Eigenvalue.dict_class_name_mapping
    print Eigenvalue.calculate_eigenvalue('C:\\cygwin64\\home\\c_youwu\\UiTest\\logs\\2017_03_27-16_31_38\\com.android.contacts\\2.uix')
    print Eigenvalue.calculate_eigenvalue('C:\\cygwin64\\home\\c_youwu\\UiTest\\logs\\2017_03_27-16_31_38\\com.android.contacts\\1.uix')