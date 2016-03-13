#!/usr/bin/pyhon
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Sep 15th, 2015
# Description: Identify registers an applying method uses and save the valuse to the corresponding fields.
#

import os

from add_id_var import *
from dynamic_judge import *
from leak_fix import *

##
# function: Find the next valid sentence.
# @param contents: Smali file's contents
# @param index: Current index
# @param direction: Upward or downward (1 for up, 2 for down)
#
def next_valid_index(contents, index, direction):
    temp_index = 1
    if 1 == direction:
        while contents[index - temp_index].isspace():
            temp_index += 1

        if contents[index - temp_index].find('.end annotation') >= 0:
            temp_index += 1
            while not contents[index - temp_index].find('.annotation') >= 0:
               temp_index += 1
            return next_valid_index(contents, index - temp_index, 1)

        return index - temp_index
    if 2 == direction:
        while contents[index + temp_index].isspace():
            temp_index += 1

        if contents[index + temp_index].find('.annotation') >= 0:
            temp_index += 1
            while not contents[index + temp_index].find('.end annotation') >= 0:
               temp_index += 1
            return next_valid_index(contents, index + temp_index, 2)

        return index + temp_index

##
# function: Find all parameters of a method.
# @param param_str: The string containing paramters infomation
# @return: A sequence of paramters
#
def get_param_seq(param_str):
    result = []

    index = 0
    start_index = 0
    is_end = True
    is_ref = False
    while index < len(param_str):
        if is_end:
            start_index = index
            is_end = False

        if 'L' == param_str[index] and not is_ref:
            is_ref = True
            index += 1
        elif not '[' == param_str[index] and not is_ref:
            is_end = True
            result.append(param_str[start_index:index+1])
            if 'J' == param_str[index] or 'D' == param_str[index]:
                result.append(' ')
            index += 1
        elif ';' == param_str[index]:
            is_end = True
            is_ref = False
            result.append(param_str[start_index:index+1])
            index += 1
        else:
            index += 1

    return result

##
# function: Find the variable type stored in the specific register.
# @param reg_position: The register position
# @param content_str: The string to be analyzed
# @return: The varibale type
#
def get_reg_type(reg_position, content_str):
    method_str = content_str.strip(' \n').split(' ')[-1]
    if 0 == reg_position:
        return method_str.split('->')[0]
    else:
        param_seq = get_param_seq(method_str.split('(')[1].split(')')[0])
        return param_seq[reg_position - 1]

##
# function: Track registers an applying method uses
# @param smali_folder: Smali folder path
# @param all_res: All leaked resources
# @param res_info: The leaked resource or the release info
# @param flag: Distinguish different resources in a funciton
# @param res_type: The type of the parameter res_info
# @param main_act: The main activity
#
def track_registers(smali_folder, all_res, res_info, flag, res_type, main_act):
    reg_need_track = []
    
    if 'LeakedRes' == res_type:
        for each in res_info.get_arg_from():
            reg_need_track.append(int(each))

        target_op = res_info.get_apply_func()

    if 'RelInfo' == res_type:
        target_op = res_info.get_release_func()

    res_identity = []

    smali_file = open(smali_folder + os.path.sep + res_info.get_func_path(), 'r')
    try:
        smali_file_contents = smali_file.readlines()
    finally:
        smali_file.close()

    for index, content in enumerate(smali_file_contents):
        if content.find('.method') >= 0 and content.find(res_info.get_func_name()) >= 0:
            temp_index = index + 1
            temp_flag = flag
            while not 0 == temp_flag:
                while smali_file_contents[temp_index].find(target_op) < 0 or smali_file_contents[temp_index].find('invoke') < 0:
                    temp_index += 1

                temp_flag -= 1
                temp_index += 1

            temp_index -= 1

            method_str = res_info.get_func_name().split('(')[0].strip('<>')
            target_op_class = target_op.split('/')[-1].split(';->')[0]
            target_op_str = target_op.split('/')[-1].split(';->')[1].split('(')[0]

            if 'LeakedRes' == res_type:
                if 'Landroid/location/LocationManager;->requestLocationUpdates(' == res_info.get_apply_func():
                    if smali_file_contents[temp_index].find('(L') >= 0:
                        apply_func_str = 'Landroid/location/LocationManager;->requestLocationUpdates(L'
                    elif smali_file_contents[temp_index].find('(J') >= 0:
                        apply_func_str = 'Landroid/location/LocationManager;->requestLocationUpdates(J'
                    else:
                        print('---> ERROR: should be \"L\" or \"J\"')
                    res_info.set_apply_func(apply_func_str)

                    for each in res_info.get_arg_from():
                        reg_need_track.append(int(each))
                elif 'Landroid/os/RemoteCallbackList;->register(' == res_info.get_apply_func():
                    t_type = smali_file_contents[temp_index].split('(')[1].split(')')[0]
                    res_info.set_rel_func(res_info.get_rel_func().replace('*', t_type))

            if 'RelInfo' == res_type:
                reg_str = smali_file_contents[temp_index].split('{')[1].split('}')[0]

                if '' == reg_str:
                    reg_num = 0
                else:
                    reg_num = len(reg_str.split(','))

                for i in range(reg_num):
                    reg_need_track.append(i)

            dy_index = temp_index
            var_index = temp_index
            acquire_line = smali_file_contents[temp_index]
            if smali_file_contents[temp_index].find('<init>') >= 0:
                var_index = next_valid_index(smali_file_contents, var_index, 2)

            for reg in reg_need_track:
                # We need the return-value of this method, as 'mCamera = Camera.open();'.
                if -1 == reg:
                    return_type = acquire_line.strip(' \n').split(')')[1]
                    field_id = 'id_' + method_str + '_' + target_op_class + '_' + target_op_str.strip('<>') + '_' + str(flag) + '_00'

                    add_static_field(smali_file_contents, field_id, return_type)
                    res_identity.append(field_id + ':' + return_type)

                    var_index = next_valid_index(smali_file_contents, var_index, 2)
                    if smali_file_contents[var_index].find('move-result-object') >= 0:
                        register = smali_file_contents[var_index].strip('\n').strip(' ').split(' ')[1]

                        new_sentences = []
                        op_arg = register + ', L' + res_info.get_func_path()[:-6] + ';->' + field_id + ':' + return_type +'\n'
                        add_op_sentence(return_type, new_sentences, 'sput', op_arg)
                        new_sentences.append('\n')

                        smali_file_contents[var_index + 1:var_index + 1] = new_sentences

                        dy_index = next_valid_index(smali_file_contents, var_index, 2)
                        var_index = next_valid_index(smali_file_contents, var_index, 2)
                    else:
                        print('---> ERROR: static => not find \"move-result-object\"')

                # Other patterns.
                else: 
                    register_str = acquire_line.split('{')[1].split('}')[0]

                    if acquire_line.find('/range') < 0:
                        track_reg = register_str.split(',')[reg].strip(' ')
                    else:
                        base_reg = acquire_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                        track_reg = base_reg[0] + str(int(base_reg[1:]) + reg)

                    reg_type = get_reg_type(reg, acquire_line)
                    field_id = 'id_' + method_str + '_' + target_op_class + '_' + target_op_str.strip('<>') + '_' + str(flag) + '_' + str(reg)

                    add_static_field(smali_file_contents, field_id, reg_type)
                    res_identity.append(field_id + ':' + reg_type)

                    new_sentences = []
                    op_arg = track_reg + ', L' + res_info.get_func_path()[:-6] + ';->' + field_id + ':' + reg_type +'\n'
                    add_op_sentence(reg_type, new_sentences, 'sput', op_arg)
                    new_sentences.append('\n')

                    temp_next_index = next_valid_index(smali_file_contents, var_index, 2)
                    if smali_file_contents[temp_next_index].find('move-result') >= 0:
                        dy_index = next_valid_index(smali_file_contents, dy_index, 2)

                    smali_file_contents[var_index:var_index] = new_sentences

                    var_index = next_valid_index(smali_file_contents, var_index, 2)
                    dy_index = next_valid_index(smali_file_contents, dy_index, 2)


                res_info.set_identity(res_identity)

            # Add dynamically judge sentences.
            offset = add_dynamic_judge(smali_file_contents, dy_index + 1, main_act, res_info, res_type)

            # If the resource has a priority and this is a release operation, add specific release operations before this release operaion.
            add_special_release_op(smali_file_contents, temp_index + offset, all_res, main_act, res_info, res_type)

            break

    smali_file = open(smali_folder + os.path.sep + res_info.get_func_path(), 'w')
    try:
        smali_file.writelines(smali_file_contents)
    finally:
        smali_file.close()
