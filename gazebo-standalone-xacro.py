# -*- coding: utf-8 -*-
""" Created on Thu Jun 30 03:29:25 2022 @author: Henrique Hafner Ferreira """

import xml.etree.ElementTree as et
import json

def fill_xml_obj(xml_obj,data_dic):
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
            elif element_text_key != '\n':
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
                elif curr_value != '\n':
                    print('No key_attribute found in data_dic for: ',curr_value)
    if len(data_dic_unused_keys)>0:
        print('The following keys were not used to fill any value: ',data_dic_unused_keys)
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

def load_data(data_path):
    with open(data_path) as dt:
        data_stringfied = dt.read()
        data = json.loads(data_stringfied)
    return data
#data = {'name_value':'name','type_value':'type','parent_value':'parent','child_value':'child','pose_value':'pose','axis_value':'axis','not_used_test':'not_used_test','mass_value':'filled!','inertiatensor_value':'filled!','inertiatensor_value':'filled!','visualname_value':'filled!','meshpath_value':'filled!'} 

model_xml_obj = et.parse('model_template.sdf')
model_rootelem = model_xml_obj.getroot()
gazebo_model_data = load_data('gazebo_model_pythondata.json')
for data_index in len(gazebo_model_data):
    if data_index == 0:
        for link_data in gazebo_model_data[data_index]
        link_template  = et.parse('link_template.sdf')
        link_xml_obj = fill_xml_obj(link_template,data)
    
    joint_template = et.parse('joint_template.sdf')
    joints_xml_obj = fill_xml_obj(joint_template,data)



model_rootelem.append(link_xml_obj.getroot())
model_rootelem.append(joints_xml_obj.getroot())
indent(model_rootelem)
model_xml_obj.write('model-links-joint.sdf')
