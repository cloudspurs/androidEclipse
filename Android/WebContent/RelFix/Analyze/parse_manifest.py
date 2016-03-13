#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Oct 12st, 2015
# Description: Parse the AndroidManifest.xml file.
#

import os
import xml.dom.minidom

##
# Class: Get informations from AndroidManifest.xml file.
#
class ManifestParser(object):
    ##
    # function: Constructor.
    # @param file_path: The AndroidManifest.xml file's path
    #
    def __init__(self, file_path):
        if not hasattr(self, '_ManifestParser__contents'):
            self.__contents = self.__obtain_xml_contents(file_path)

    ##
    # function: This method for creating a Singleton.
    #
    def __new__(cls, file_path):
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls, file_path)

        return cls.instance

    ##
    # function: Get contents of the xml file.
    # @param file_path: The xml file path
    # @return: The contents
    #
    def __obtain_xml_contents(self, file_path):
        return xml.dom.minidom.parse(file_path)

    ##
    # function: Get the main activity.
    # @return: The main activity
    #
    def get_main_act(self):
        root = self.__contents.documentElement
        package_name = root.getAttribute('package')

        act_list = root.getElementsByTagName('activity')
        for each_act in act_list:
            intent_filter_list = each_act.getElementsByTagName('intent-filter')
            if len(intent_filter_list) > 0:
                intent_filter = intent_filter_list[0]

                action_list = intent_filter.getElementsByTagName('action')
                for each_action in action_list:
                    if 'android.intent.action.MAIN' == each_action.getAttribute('android:name'):
                        main_act_name = each_act.getAttribute('android:name')
                        if '.' == main_act_name[0]:
                            return (package_name + main_act_name).replace('.', '/')
                        elif main_act_name.find('.') < 0:
                            return (package_name + '.' + main_act_name).replace('.', '/')
                        else:
                            return main_act_name.replace('.', '/')

        return 'parse AndroidManifest error'

    ##
    # function: Find all activities in the app.
    # @return: A list contains all activities
    #
    def get_all_act(self):
        result = [] 

        root = self.__contents.documentElement
        package_name = root.getAttribute('package')

        act_list = root.getElementsByTagName('activity')
        for each_act in act_list:
            result.append(each_act.getAttribute('android:name'))

        for index, each_act_name in enumerate(result):
            if '.' == each_act_name[0]:
                result[index] = package_name + result[index]
            elif each_act_name.find('.') < 0:
                result[index] = package_name + '.' +result[index]

        for i in range(len(result)):
            result[i] = result[i].replace('.', '/')

        return result

    ##
    # function: Find all services in the app.
    # @return: A list contains all services
    #
    def get_all_ser(self):
        result = [] 

        root = self.__contents.documentElement
        package_name = root.getAttribute('package')

        ser_list = root.getElementsByTagName('service')
        for each_ser in ser_list:
            result.append(each_ser.getAttribute('android:name'))

        for index, each_ser_name in enumerate(result):
            if '.' == each_ser_name[0]:
                result[index] = package_name + result[index]
            elif each_ser_name.find('.') < 0:
                result[index] = package_name + '.' +result[index]

        for i in range(len(result)):
            result[i] = result[i].replace('.', '/')

        return result

##
# fucntion: Modify the manifest file to add some permission.
# @param path: The manifest file path
#
def modify_manifest(path):
    manifest_file = open(path, 'r')
    try:
        file_contents = manifest_file.readlines()
    finally:
        manifest_file.close()

    # permission: GET_TASKS
    for index, each_line in enumerate(file_contents):
        if each_line.find('uses-permission android:name=\"android.permission.GET_TASKS\"') >= 0:
            break

        if each_line.find('</manifest>') >= 0:
            new_sentences = []
            new_sentences.append('    <uses-permission android:name=\"android.permission.GET_TASKS\"/>')

            file_contents[index:index] = new_sentences
            break

    manifest_file = open(path, 'w')
    try:
        manifest_file.writelines(file_contents)
    finally:
        manifest_file.close()


