# -*- coding: utf-8 -*-
""" Created on Thu Jun 30 03:29:25 2022 @author: Henrique Hafner Ferreira """

import xml.etree.ElementTree as et
import copy
import json

def val_chk(valin):
    valin = valin.replace(' ','')
    if valin[-6:] != '_value':
        return False
    return True

def fill_xml_obj(xml_obj, data_dic):
    data_dic_unused_keys = list(data_dic.keys())
    tree_root = xml_obj.getroot()
    for element in tree_root.iter():
        element_text_key = element.text
        if element_text_key:
            element_text_key = element_text_key.replace(' ','')
            if element_text_key in data_dic:
                element.text = data_dic[element_text_key]
                if data_dic_unused_keys.count(element_text_key):
                    data_dic_unused_keys.remove(element_text_key)
            elif element_text_key != '\n' and val_chk(element_text_key):
                print('No key_text found in data_dic for: ',element_text_key)

        keys_attribute = element.attrib.keys()
        if len(keys_attribute) > 0:
            for curr_key in keys_attribute:
                curr_value = element.attrib[curr_key]
                curr_value = curr_value.replace(' ','')
                if curr_value in data_dic:
                    element.attrib[curr_key] = data_dic[curr_value]
                    if data_dic_unused_keys.count(curr_value):
                        data_dic_unused_keys.remove(curr_value)
                elif curr_value != '\n' and not val_chk(curr_value):
                    print('No key_attribute found in data_dic for: ',curr_value)
    if len(data_dic_unused_keys)>0:
        print('The following keys were not used to fill any value: ',data_dic_unused_keys)
        print()
    return xml_obj

def indent(elem, level=0):  
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def json_data_get(file_path ):
    with open(file_path) as dt:
        data_stringfied = dt.read()
        data = json.loads(data_stringfied)
    return data

def get_model_json_data(folder_path='' ):
    file_path = 'gazebo_model_pythondata.json'
    gazebo_model_data = json_data_get(file_path)
    return gazebo_model_data

def build_model_sdf_data(model_data):
    model_xml_obj  = et.parse('model_template.xml')
    link_template  = et.parse('link_template.xml' )
    joint_template = et.parse('joint_template.xml')
    model_rootelem = model_xml_obj.getroot()
    #build links
    links_data  = model_data[0]
    for link_values in links_data:
        link_xml  = copy.deepcopy(link_template)
        link_xml_filled = fill_xml_obj(link_xml,link_values)
        model_rootelem.append(link_xml_filled.getroot())
    #build joints
    joint_data = model_data[1]
    for joint_values in joint_data:
        joint_xml = copy.deepcopy(joint_template)
        joints_xml_filled = fill_xml_obj(joint_xml,joint_values)
        model_rootelem.append(joints_xml_filled.getroot())
    #build model section
    indent(model_rootelem)
    model_xml_obj.write('model_links_joint.xml')
    return True

