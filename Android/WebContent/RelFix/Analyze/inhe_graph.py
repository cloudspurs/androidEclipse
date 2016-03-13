#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Dec 16th, 2015
# Description: Build inheritance graph.
#

import os

##
# Class: Build inheritance graph.
#
class InheGraph(object):
    ##
    # function: Constructor.
    # @param smali_folder: The smali folder path
    #
    def __init__(self, smali_folder):
        if not hasattr(self, '_InheTree__graph'):
            self.__graph = {}
            self.__smali_folder = smali_folder
            self.__build_graph('')

    ##
    # function: This method for creating a Singleton.
    #
    def __new__(cls, smali_folder):
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls, smali_folder)

        return cls.instance

    ##
    # function: Build the graph recursively.
    # @param path: The target path
    #
    def __build_graph(self, path):
        if '/android' == path or path.find('/R.smali') >= 0 or path.find('R$') >= 0 or path.find('/BuildConfig.smali') >= 0:
            return

        if os.path.exists(self.__smali_folder + os.path.sep + path):
            if os.path.isdir(self.__smali_folder + os.path.sep + path):
                for item in os.listdir(self.__smali_folder + os.path.sep + path):
                    self.__build_graph(path + os.path.sep + item)
            else:
                smali_file = open(self.__smali_folder + os.path.sep + path)
                try:
                    file_content = smali_file.readlines()
                finally:
                    smali_file.close()

                for each_line in file_content:
                    if each_line.find('.class') == 0:
                        class_name = each_line.strip(' \n').split(' ')[-1]
                    elif each_line.find('.super') == 0 and not 'Ljava/lang/Object;' == each_line.strip(' \n').split(' ')[-1]:
                        if not each_line.strip(' \n').split(' ')[-1] in self.__graph:
                            self.__graph[each_line.strip(' \n').split(' ')[-1]] = []
                        self.__graph[each_line.strip(' \n').split(' ')[-1]].append(class_name)
                    elif each_line.find('.implements') == 0:
                        if not each_line.strip(' \n').split(' ')[-1] in self.__graph:
                            self.__graph[each_line.strip(' \n').split(' ')[-1]] = []
                        self.__graph[each_line.strip(' \n').split(' ')[-1]].append(class_name)


    ##
    # function: Other objects get the graph from this method.
    # @return: The dictionary storing the graph 
    #
    def get_graph(self):
        return self.__graph
