#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Oct 12th, 2015
# Description: This file contains a class which stores the informations of a release operation.
#

##
# Class: Store the information of a specific release operation.
#
class RelInfo:
    ##
    # function: Constructor.
    # @param func_path: Smali file path
    # @param func_name: The function where the resource applys
    # @param release_func: The method which releases a resource
    #
    def __init__(self, func_path, func_name, release_func):
        # Smali file path.
        self.__func_path = func_path
        # The function where the resource applys.
        self.__func_name = func_name
        # Method releasing the resource.
        self.__release_function = release_func
        # Distinguish different resource object with the same resource type.
        self.__identity = []

    ##
    # function: Set identity.
    # @param: The identity
    #
    def set_identity(self, id):
        self.__identity = id

    ##
    # function: Get the identity.
    # @param: The identity
    #
    def get_identity(self):
        return self.__identity

    ##
    # function: Get the smali file path.
    # @return: The path
    #
    def get_func_path(self):
        return self.__func_path

    ##
    # function: Get the function where the resource applys.
    # @return: The function name
    #
    def get_func_name(self):
        return self.__func_name

    ##
    # function: Get the release method's name.
    # @return: The method name
    #
    def get_release_func(self):
        return self.__release_function


