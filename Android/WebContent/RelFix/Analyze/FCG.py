#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Aug 24th, 2015
# Description: Construct FCG.
#

import os

##
# Class: Construct FCG.
#
class FCG(object):
    ##
    # function: Constructor.
    # @param smali_folder: The smali folder path
    # @param inhe_graph: The inheritance graph 
    #
    def __init__(self, smali_folder, inhe_graph):
        if not hasattr(self, '_FCG__fcg'):
            self.__fcg = {}
            self.__rfcg = {}
            self.__smali_folder = smali_folder
            self.__inhe_graph = inhe_graph
            self.__get_methods('')
            self.__obtain_fcg('')

    ##
    # function: This method for creating a Singleton.
    #
    def __new__(cls, smali_folder, inhe_graph):
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls, smali_folder, inhe_graph)

        return cls.instance

    ##
    # function: Get all user-defined methods.
    # @param path: The target path
    #
    def __get_methods(self, path):
        if '/android' == path:
            return

        if os.path.exists(self.__smali_folder + os.path.sep + path):
            if os.path.isdir(self.__smali_folder + os.path.sep + path):
                for item in os.listdir(self.__smali_folder + os.path.sep + path):
                    self.__get_methods(path + os.path.sep + item)
            else:
                smali_file = open(self.__smali_folder + os.path.sep + path)
                try:
                    file_content = smali_file.readlines()
                finally:
                    smali_file.close()

                if len(file_content) < 3:
                    return
                if '.source \"R.java\"' == file_content[2] or '.source \"BuildConfig.java\"' == file_content[2]:
                    return

                class_name = file_content[0].strip(' \n').split(' ')[-1]
                method = ''
                for each_line in file_content:
                    if each_line.find('.method') == 0:
                        method = each_line.strip(' \n').split(' ')[-1]
                        self.__fcg[class_name + '->' + method] = []
                        self.__rfcg[class_name + '->' + method] = []

    ##
    # function: Add inheritance info into the FCG.
    # @param caller: The caller method
    # @param callee: The callee method
    #
    def __add_inhe(self, caller, callee):
        if not callee.split('->')[0] in self.__inhe_graph:
            return

        for child in self.__inhe_graph[callee.split('->')[0]]:
            if child + '->' + callee.split('->')[1] in self.__fcg:
                if not child + '->' + callee.split('->')[1] in self.__fcg[caller]:
                    self.__fcg[caller].append(child + '->' + callee.split('->')[1])
                if not caller in self.__fcg[child + '->' + callee.split('->')[1]]:
                    self.__rfcg[child + '->' + callee.split('->')[1]].append(caller)

            self.__add_inhe(caller, child + '->' + callee.split('->')[1])

    ##
    # function: Obtain the FCG which uses a dictionary to store the construction.
    # @param path: The target path 
    #
    def __obtain_fcg(self, path):
        if "/android" == path:
            return

        if os.path.exists(self.__smali_folder + os.path.sep + path):
            if os.path.isdir(self.__smali_folder + os.path.sep + path):
                for item in os.listdir(self.__smali_folder + os.path.sep + path):
                    self.__obtain_fcg(path + os.path.sep + item)
            else:
                smali_file = open(self.__smali_folder + os.path.sep + path)
                try:
                    file_content = smali_file.readlines()
                finally:
                    smali_file.close()

                class_name = file_content[0].strip(' \n').split(' ')[-1]
                method = ''
                for each_line in file_content:
                    if each_line.find('.method') == 0:
                        method = each_line.strip(' \n').split(' ')[-1]
                    elif each_line.find('invoke-') >= 0:
                        callee_method = each_line.strip(' \n').split(' ')[-1]
                        if callee_method in self.__fcg:
                            if not callee_method in self.__fcg[class_name + '->' + method]:
                                self.__fcg[class_name + '->' + method].append(callee_method)
                            if not class_name + '->' + method in self.__rfcg[callee_method]:
                                self.__rfcg[callee_method].append(class_name + '->' + method)
                            # Consider the inheritance.
                            self.__add_inhe(class_name + '->' + method, callee_method)


    ##
    # function: Other objects get the FCG from this method.
    # @return: The dictionary storing the FCG information 
    #
    def get_FCG(self):
        return self.__fcg

    ##
    # function: Other objects get the rFCG from this method.
    # @return: The dictionary storing the rFCG information 
    #
    def get_rFCG(self):
        return self.__rfcg
