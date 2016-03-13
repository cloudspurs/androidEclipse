#!usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Sep 2nd, 2015
# Description: A class containing the informations about resources in Android system. These informations refer to 'resource_table' file.
#

from Analyze.constant import * 

##
# Class: Get contents in 'resource_table' file.
#
class InfoTable(object):
    ##
    # function: Constructor.
    #
    def __init__(self):
        if not hasattr(self, '_InfoTable__res_info'):
            self.__res_info = self.__get_info_from_file()

    ##
    # function: This method for creating a Singleton.
    #
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls)

        return cls.instance

    ##
    # function: Get the 'resource_table' file's contents.
    # @return: All resources' info stored in a dictionary
    #
    def __get_info_from_file(self):
        resource_table_file = open(Constants._resource_table_path, 'r')
        try:
            file_contents = resource_table_file.readlines()
        finally:
            resource_table_file.close()

        all_info = {} 

        for each_line_content in file_contents:
            each_elements = each_line_content.strip('\n').split(':')

            for index, element in enumerate(each_elements):
                if 0 == index:
                    all_info[element] = []
                else:
                    all_info[each_elements[0]].append(element)

        return all_info

    ##
    # function: Other objects get the information from this method.
    # @return: All resources' info stored in a dictionary
    #
    def get(self):
        return self.__res_info

