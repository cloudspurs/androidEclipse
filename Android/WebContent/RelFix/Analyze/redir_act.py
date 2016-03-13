#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Dec 18st, 2015
# Description: Redirect fix code inserting place.
#

import os

##
# function: Redirect fix code inserting place.
# @param act_list: The original Activity list
# @param smali_folder: The smali folder path
# @return: The redirect result info
#
def redirect_act(act_list, smali_folder):
    result = {}
    for each_act in act_list:
        act_file = open(smali_folder + os.path.sep + each_act + '.smali', 'r')
        try:
            file_contents = act_file.readlines()
        finally:
            act_file.close()

        if file_contents[1].find('Landroid/') >= 0:
            result['L' + each_act + ';'] = 'L' + each_act + ';'
        else:
            super_class = file_contents[1].strip(' \n').split(' ')[-1][1:-1]
            done = False
            while not done:
                act_file = open(smali_folder + os.path.sep + super_class + '.smali', 'r')
                try:
                    file_contents = act_file.readlines()
                finally:
                    act_file.close()

                find_method = False
                for each_line in file_contents:
                    if each_line.find('.method') >= 0 and each_line.find('onDestroy') >= 0:
                        find_method = True
                        if each_line.find('final') < 0:
                            result['L' + each_act + ';'] = 'L' + each_act + ';'
                        else:
                            result['L' + each_act + ';'] = 'L' + super_class + ';'
                        done = True
                        break

                if not find_method:
                    if file_contents[1].find('Landroid/') >= 0:
                        result['L' + each_act + ';'] = 'L' + each_act + ';'
                        done = True
                    else:
                        super_class = file_contents[1].strip(' \n').split(' ')[-1][1:-1]

    return result

##
# function: Delete non-exist Activities.
# @param act_list: The original Activity list
# @param smali_folder: The smali folder path
# @return: The new Activity list
#
def check_act(act_list, smali_folder):
    result = []
    for each_act in act_list:
        if os.path.exists(smali_folder + os.path.sep + each_act + '.smali'):
            result.append(each_act)

    return result

