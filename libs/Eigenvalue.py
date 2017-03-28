# -*- encoding:UTF-8 -*-
import re
from xml.etree.ElementTree import ElementTree, Element
from GlobalVariable import GlobalVariable


class Eigenvalue(object):
    dict_class_name_mapping_id = dict()

    @staticmethod
    def __get_dict_of_number_map_letter(upper=True):
        count = 0
        dict_tmp = dict()
        letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if not upper:
            letter = letter.lower()
        for s in letter:
            dict_tmp[count]=s
            count += 1
        return dict_tmp

    dict_number_map_upper_letter = __get_dict_of_number_map_letter.__func__(upper=True)
    #dict_number_map_lower_letter = __get_dict_of_number_map_letter.__func__(upper=False)

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

    #dict_upper_letter_map_number = __get_dict_of_letter_map_number.__func__(upper=True)
    dict_lower_letter_map_number = __get_dict_of_letter_map_number.__func__(upper=False)

    @staticmethod
    def convert_26_to_10(x):
        x = x.lower()
        x1 = Eigenvalue.dict_lower_letter_map_number.get(x[0])
        x2 = Eigenvalue.dict_lower_letter_map_number.get(x[1])
        return x1 * 26 + x2

    @staticmethod
    def convert_10_to_26(x):
        x = int(x)
        x1 = x / 26
        x2 = x % 26
        return Eigenvalue.dict_number_map_upper_letter.get(x1) + Eigenvalue.dict_number_map_upper_letter.get(x2)


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
        element = Element('class', {'name': class_name, 'id': class_id, 'code': '' })
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
        # if len(sequence) > 60:
        #     return sequence[:60]
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

    print Eigenvalue.dict_lower_letter_map_number

    print Eigenvalue.convert_26_to_10('dd')
    print Eigenvalue.convert_10_to_26(81)