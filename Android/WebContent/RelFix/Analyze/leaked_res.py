#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Aug 31st, 2015
# Description: This file contains a class which stores the informations of a leaked resource.
#

from info_table import *

##
# Class: Store the information of a specific leaked resource.
#
class LeakedRes:
    ##
    # function: Constructor.
    # @param func_path: Smali file path
    # @param func_name: The function where the resource applys
    # @param apply_func: The method which applies a resource
    #
    def __init__(self, func_path, func_name, apply_func):
        # Smali file path.
        self.__func_path = func_path
        # The function where the resource applys.
        self.__func_name = func_name
        # Method applying the resource.
        self.__apply_function = apply_func
        # Distinguish different resource object with the same resource type.
        self.__identity = []
        # Method releasing the resource.
        self.__release_function = ''
        # The resource should be released here.
        self.__suggested_release_place = ''
        # Where to find the arguments the release method need.
        self.__release_arg_from = []
        # Indicate a releasing order for some release methods.
        self.__priority = ''
        # A method of a entrance point in FCG.
        self.__backward_trace_function = []

        if not 'Landroid/location/LocationManager;->requestLocationUpdates(' == apply_func:
            self.__set_release_func()
            self.__set_suggested_release_place()
            self.__set_release_arg_from()
            self.__set_priority()
            
    ##
    # function: Obtain the corresponding release method name from the specific resource.
    #
    def __set_release_func(self):
        self.__release_function = InfoTable().get()[self.__apply_function][0]

    ##
    # function: Obtain the place where the specific resource should be released. The place is one of onPause(), onStop() and onDestroy() referring to Android API.
    #
    def __set_suggested_release_place(self):
        self.__suggested_release_place = InfoTable().get()[self.__apply_function][1]

    ##
    # function: Obtain the index numbers which represent the position of arguments in applying function also used in release function.
    #
    def __set_release_arg_from(self):
        self.__release_arg_from = InfoTable().get()[self.__apply_function][2:-1]
        
    ##
    # function: Obtain the priority of a applying method. A higher priority, a later releasing place.
    #
    def __set_priority(self):
        self.__priority = InfoTable().get()[self.__apply_function][-1]

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
    # function: Set the apply function.
    # @param apply_func_str: The apply funcion
    #
    def set_apply_func(self, apply_func_str):
        self.__apply_function = apply_func_str

        self.__set_release_func()
        self.__set_suggested_release_place()
        self.__set_release_arg_from()
        self.__set_priority()

    ##
    # function: Get the apply method's name.
    # @return: The method name
    #
    def get_apply_func(self):
        return self.__apply_function

    ##
    # function: Set identity.
    # @param id: The identity
    #
    def set_identity(self, id):
        self.__identity = id

    ##
    # function: Get the identity.
    # @return: The identity
    #
    def get_identity(self):
        return self.__identity

    ##
    # function: Set the release method's name.
    # @param rel_func: The release metbod
    #
    def set_rel_func(self, rel_func):
        self.__release_function = rel_func

    ##
    # function: Get the release method's name.
    # @return: The method name
    #
    def get_rel_func(self):
        return self.__release_function

    ##
    # function: Get the place where suggested to release the resource.
    # @return: one of the three life-cycle callback methods
    #
    def get_suggested_rel_place(self):
        return self.__suggested_release_place

    ##
    # function: Get the information that where to find arguments of release method.
    # @return: A array whose length equals the parameters' number of release function
    #
    def get_arg_from(self):
        return self.__release_arg_from

    ##
    # function: Get the priority of the method.
    # @return: The priority
    #
    def get_priority(self):
        return self.__priority

    ##
    # function: Set backward trace method name.
    # @param: The method name
    #
    def set_trace_func(self, func):
        self.__backward_trace_function = func

    ##
    # function: Get the backward trace method name.
    # @return: The method name
    #
    def get_trace_func(self):
        return self.__backward_trace_function
