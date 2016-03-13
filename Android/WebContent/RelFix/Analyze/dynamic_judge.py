#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Oct 13st, 2015
# Description: Dynamically judge the leaked resources.
#

import os

from constant import *

##
# function: Obtain the number and type of method arguments by analyzing the .method string in smali file.
# @param completed_method_line: The completed '.method' string
# @raturn: An array containing the informations.
#
def obtain_param_info(completed_method_line):
    return_value_list = []
    arg_num = 0

    if not 'static' in completed_method_line.split(' '):
        return_value_list.append(3)
        arg_num += 1

    origin_parameter_str = (completed_method_line.split('(')[1]).split(')')[0]
    index = 0
    L_flag = 0
    array_flag = 0
    while index < len(origin_parameter_str):
        char = origin_parameter_str[index]

        if '[' == char:
            if 0 == array_flag:
                array_flag = 1
                arg_num += 1
                return_value_list.append(3)
            
        if 0 == L_flag and 'L' == char:
            L_flag = 1

            if 0 == array_flag:
                arg_num += 1
                return_value_list.append(3)

        if 0 == L_flag and ('Z' == char or 'B' == char or 'S' == char or 'C' == char or 'I' == char or 'F' == char):
            if 0 == array_flag:
                arg_num += 1
                return_value_list.append(1)

            if 1 == array_flag:
                array_flag = 0

        if 0 == L_flag and ('D' == char or 'J' == char):
            if 0 == array_flag:
                arg_num += 2
                return_value_list.append(2)
                return_value_list.append(0)

            if 1 == array_flag:
                array_flag = 0

        if ';' == char:
            L_flag = 0
            array_flag = 0

        index += 1
        
    return_value_list.insert(0, arg_num)
    return return_value_list

##
# function: Transfer the parameter-registers to local-registers and then add extra local-registers to satisfy our requests.
# @param local_num: The number of local registers
# @param param_regeister_info: The information of parameter-registers
# @param content: The smali file contents
# @param start_index: The place where we insert new smali sentences in
# @return: A new index
# 
def transfer_registers(local_num, param_register_info, content, start_index):
    param_num = param_register_info[0]

    content[start_index] = '    .registers %d\n' % (local_num + param_num + 20)

    temp_index = 1
    while content[start_index + temp_index].find('.prologue') < 0:
        if content[start_index + temp_index].isspace() or content[start_index + temp_index].find('.param') >= 0:
            temp_index += 1
        else:
            temp_index -= 1
            break
    
    # Move value from p naming registers to v naming registers
    temp_index += 1
    content.insert(start_index + temp_index, '\n')
    temp_index += 1
    for i in range(param_num):
        if 1 == param_register_info[i+1]:
            content.insert(start_index + temp_index, '    move/16 v%d, p%d\n' % (local_num + i, i))
            temp_index += 1
        if 2 == param_register_info[i+1]:
            content.insert(start_index + temp_index, '    move-wide/16 v%d, p%d\n' % (local_num + i, i))
            temp_index += 1
        if 3 == param_register_info[i+1]:
            content.insert(start_index + temp_index, '    move-object/16 v%d, p%d\n' % (local_num + i, i))
            temp_index += 1
        if 0 == param_register_info[i+1]:
            continue
    content.insert(start_index + temp_index, '\n')

    new_index = start_index + temp_index

    # Transfer p naming registers to v naming registers 
    while content[start_index + temp_index].find('.end method') < 0:
        temp_index += 1
        
        for i in range(param_num):
            line_content = content[start_index + temp_index]
            target_position = line_content.find('p%d' % i)
            if target_position >= 0:
                if not line_content[target_position - 1].isalpha() and not line_content[target_position - 1].isdigit(): 
                    if not line_content[target_position + len(str(i)) + 1].isalpha() and not line_content[target_position + len(str(i)) + 1].isdigit(): 
                        content[start_index + temp_index] = line_content.replace('p%d' % i, 'v%d' % (i + local_num))

    return new_index

##
# function: Find a object register whose position is less than 16.
# @param contents: The smali file contents
# @param index: The position
# @return: The index of the register
#
def find_an_object_reg(contents, index):
    while contents[index].find('sput-object') < 0:
        index -= 1

    return int(contents[index].strip(' \n').split(' ')[1][1:-1])

##
# function: Add smali codes to dynamically judge the leaked resources.
# @param contents: The smali file contents
# @param index: The postion of adding sentences
# @param main_act: The main activity
# @param res_info: The leaked resource or the release info
# @param res_type: The type of the parameter res_info
# @return: The number of new sentences
#
def add_dynamic_judge(contents, index, main_act, res_info, res_type):
    return_num = 0
    temp_index = index

    while contents[temp_index].find('.locals') < 0 and contents[temp_index].find('.registers') < 0:
        temp_index -= 1

    label_flag = 0
    # If we find '.registers', we don't need to change registers again.
    if contents[temp_index].find('.locals') >= 0:
        local_reg_num = int(contents[temp_index].strip(' \n').split(' ')[1])

        if contents[temp_index - 1].find('.method') >= 0:
            method_sentence = contents[temp_index - 1].strip(' \n')
            param_register_info = obtain_param_info(method_sentence)

            transfer_registers(local_reg_num, param_register_info, contents, temp_index)
            index += (param_register_info[0] + 2)
            return_num += (param_register_info[0] + 2)
        else:
            print('---> ERROR: can\'t find \'.method\'')
    else:
        label_index = index

        while contents[label_index].find('.end method') < 0:
            label_index += 1

        while contents[label_index].find('.method') < 0:
            label_index -= 1

            if contents[label_index].find('relfix') >= 0 and contents[label_index].find('goto') >= 0:
                label_flag = max(label_flag, int(contents[label_index].split('_')[1]))

        label_flag += 1

    all_reg_num = int(contents[temp_index].strip(' \n').split(' ')[1])
    available_reg_index = all_reg_num - 20

    # Add dynamic-judge sentences.
    new_sentences = []
    new_line_num = 0
    if 'LeakedRes' == res_type:
        new_sentences.append('\n')
        # boolean exist = false;
        new_sentences.append('    const/16 v%d, 0x0\n' % (available_reg_index))
        new_sentences.append('    .local v%d, \"exist\":Z\n' % (available_reg_index))
        # for (int i = 0; i < ass_list.size(); i++){
        new_sentences.append('    const/16 v%d, 0x0\n' % (available_reg_index + 1))
        new_sentences.append('    .local v%d, \"i\":I\n' % (available_reg_index + 1))
        new_sentences.append('    :relfix_%d_goto_0\n' % label_flag)
        new_sentences.append('    sget-object v%d, L' % (available_reg_index + 2) + main_act + ';->' + Constants._ass_list_name + ':Ljava/util/List;\n')
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->size()I\n' % (available_reg_index + 2, available_reg_index + 2))
        new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
        new_sentences.append('    sub-int v%d, v%d, v%d\n' % (available_reg_index + 3, available_reg_index + 3, available_reg_index + 1))
        new_sentences.append('    if-lez v%d, :relfix_%d_cond_0\n' % (available_reg_index + 3, label_flag))
        #     if (ass_list.get(i).get(0).equals(<apply_function>)){
        new_sentences.append('    const-string v%d, \"' % (available_reg_index + 4) + res_info.get_apply_func() + '\"\n')
        new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
        new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
        new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
        new_sentences.append('    check-cast v%d, Ljava/util/List;\n' % (available_reg_index + 3))
        new_sentences.append('    const/16 v%d, 0x0\n' % (available_reg_index + 5))
        new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 3))
        new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 5))
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
        new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
        new_sentences.append('    check-cast v%d, Ljava/lang/String;\n' % (available_reg_index + 3))
        new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z\n' % (available_reg_index + 3, available_reg_index + 4))
        new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
        new_sentences.append('    if-eqz v%d, :relfix_%d_cond_1\n' % (available_reg_index + 3, label_flag))
        #         if (ass_list.get(i).get(4).equals(<target_object>)){
        for i in range(len(res_info.get_identity())):
            new_sentences.append('    sget-object v%d, L' % (available_reg_index + 4) + res_info.get_func_path()[:-6] + ';->' + res_info.get_identity()[i] + '\n')
            new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
            new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
            new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
            new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
            new_sentences.append('    check-cast v%d, Ljava/util/List;\n' % (available_reg_index + 3))
            new_sentences.append('    const/16 v%d, 0x%d\n' % (available_reg_index + 5, (4 + i)))
            new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 3))
            new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 5))
            new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
            new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
            new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z\n' % (available_reg_index + 3, available_reg_index + 4))
            new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
            new_sentences.append('    if-eqz v%d, :relfix_%d_cond_1\n' % (available_reg_index + 3, label_flag))
        #             exist = true;
        new_sentences.append('    const/16 v%d, 0x1\n' % (available_reg_index))
        #         }
        #     }
        new_sentences.append('    :relfix_%d_cond_1\n' % label_flag)
        new_sentences.append('    add-int/lit8 v%d, v%d, 0x1\n' % (available_reg_index + 1, available_reg_index + 1))
        new_sentences.append('    goto :relfix_%d_goto_0\n' % label_flag)
        # }
        new_sentences.append('    :relfix_%d_cond_0\n' % label_flag)
        new_sentences.append('    .end local v%d    # \"i\":I\n' % (available_reg_index + 1))

        # if (!exist){
        new_sentences.append('    if-nez v%d, :relfix_%d_cond_2\n' % (available_reg_index, label_flag))
        #     List newResAttr = new ArrayList();
        new_sentences.append('    new-instance v%d, Ljava/util/ArrayList;\n' % (available_reg_index + 1))
        new_sentences.append('    invoke-direct/range {v%d .. v%d}, Ljava/util/ArrayList;-><init>()V\n' % (available_reg_index + 1, available_reg_index + 1))
        new_sentences.append('    .local v%d, \"newResAttr\":Ljava/util/List;\n' % (available_reg_index + 1))
        #     newResAttr.add(<apply_function>);
        new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 1))
        new_sentences.append('    const-string v%d, \"' % (available_reg_index + 7) + res_info.get_apply_func() + '\"\n')
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->add(Ljava/lang/Object;)Z\n' % (available_reg_index + 6, available_reg_index + 7))
        #     newResAttr.add(<release_function>);
        new_sentences.append('    const-string v%d, \"' % (available_reg_index + 7) + res_info.get_rel_func() + '\"\n')
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->add(Ljava/lang/Object;)Z\n' % (available_reg_index + 6, available_reg_index + 7))
        #     newResAttr.add(<component_name>);
        new_sentences.append('    sget-object v%d, L' % (available_reg_index + 8) + main_act + ';->' + Constants._ass_act_manager_name + ':Landroid/app/ActivityManager;\n')
        new_sentences.append('    const/16 v%d, 0x1\n' % (available_reg_index + 9))
        new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Landroid/app/ActivityManager;->getRunningTasks(I)Ljava/util/List;\n' % (available_reg_index + 8, available_reg_index + 9))
        new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 8))
        new_sentences.append('    const/16 v%d, 0x0\n' % (available_reg_index + 9))
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 8, available_reg_index + 9))
        new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 8))
        new_sentences.append('    check-cast v%d, Landroid/app/ActivityManager$RunningTaskInfo;\n' % (available_reg_index + 8))

        if available_reg_index + 8 < 16:
            new_sentences.append('    iget-object v%d, v%d, Landroid/app/ActivityManager$RunningTaskInfo;->topActivity:Landroid/content/ComponentName;\n' % (available_reg_index + 8, available_reg_index + 8))
            new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Landroid/content/ComponentName;->getClassName()Ljava/lang/String;\n' % (available_reg_index + 8, available_reg_index + 8))
            new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 7))
        else:
            object_reg_index = find_an_object_reg(contents, index)
            new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 9, object_reg_index))
            new_sentences.append('    move-object/16 v%d, v%d\n' % (object_reg_index, available_reg_index + 8))
            new_sentences.append('    iget-object v%d, v%d, Landroid/app/ActivityManager$RunningTaskInfo;->topActivity:Landroid/content/ComponentName;\n' % (object_reg_index, object_reg_index))
            new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Landroid/content/ComponentName;->getClassName()Ljava/lang/String;\n' % (object_reg_index, object_reg_index))
            new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 7))
            new_sentences.append('    move-object/16 v%d, v%d\n' % (object_reg_index, available_reg_index + 9))

            new_line_num += 2

        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->add(Ljava/lang/Object;)Z\n' % (available_reg_index + 6, available_reg_index + 7))
        #     newResAttr.add(<id_num>);
        new_sentences.append('    const/16 v%d, 0x%d\n' % (available_reg_index + 7, len(res_info.get_identity())))
        new_sentences.append('    invoke-static/range {v%d .. v%d}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;\n' % (available_reg_index + 7, available_reg_index + 7))
        new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 7))
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->add(Ljava/lang/Object;)Z\n' % (available_reg_index + 6, available_reg_index + 7))
        #     newResAttr.add(<id_value>);
        for i in range(len(res_info.get_identity())):
            new_sentences.append('    sget-object v%d, L' % (available_reg_index + 7) + res_info.get_func_path()[:-6] + ';->' + res_info.get_identity()[i] + '\n')
            new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->add(Ljava/lang/Object;)Z\n' % (available_reg_index + 6, available_reg_index + 7))
        #     ass_list.add(newResAttr);
        new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
        new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->add(Ljava/lang/Object;)Z\n' % (available_reg_index + 6, available_reg_index + 7))
        #     Log.i("RelFix_apply", "<apply_func>");
        new_sentences.append('    const-string v%d, \"RelFix_acquire\"\n' % (available_reg_index + 6))
        new_sentences.append('    const-string v%d, \"%s\"\n' % (available_reg_index + 7, res_info.get_apply_func()))
        new_sentences.append('    invoke-static/range {v%d .. v%d}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I\n' % (available_reg_index + 6, available_reg_index + 7))
        # }
        new_sentences.append('    .end local v%d    # \"newResAttr\":Ljava/util/List;\n' % (available_reg_index + 1))
        new_sentences.append('    :relfix_%d_cond_2\n' % label_flag)
        new_sentences.append('\n')

        contents[index:index] = new_sentences
        new_line_num += len(res_info.get_identity()) * 16 + 66
        index += new_line_num
    elif 'RelInfo' == res_type:
        new_sentences.append('\n')
        # for (int i = 0; i < ass_list.size(); i++){
        new_sentences.append('    const/16 v%d, 0x0\n' % (available_reg_index + 1))
        new_sentences.append('    .local v%d, \"i\":I\n' % (available_reg_index + 1))
        new_sentences.append('    :relfix_%d_goto_0\n' % label_flag)
        new_sentences.append('    sget-object v%d, L' % (available_reg_index + 2) + main_act + ';->' + Constants._ass_list_name + ':Ljava/util/List;\n')
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->size()I\n' % (available_reg_index + 2, available_reg_index + 2))
        new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
        new_sentences.append('    sub-int v%d, v%d, v%d\n' % (available_reg_index + 3, available_reg_index + 3, available_reg_index + 1))
        new_sentences.append('    if-lez v%d, :relfix_%d_cond_0\n' % (available_reg_index + 3, label_flag))
        #     if (ass_list.get(i).get(1).contains(<release_function>)){
        new_sentences.append('    const-string v%d, \"' % (available_reg_index + 4) + res_info.get_release_func() + '\"\n')
        new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
        new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
        new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
        new_sentences.append('    check-cast v%d, Ljava/util/List;\n' % (available_reg_index + 3))
        new_sentences.append('    const/16 v%d, 0x1\n' % (available_reg_index + 5))
        new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 3))
        new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 5))
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
        new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
        new_sentences.append('    check-cast v%d, Ljava/lang/String;\n' % (available_reg_index + 3))
        new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z\n' % (available_reg_index + 3, available_reg_index + 4))
        new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
        new_sentences.append('    if-eqz v%d, :relfix_%d_cond_1\n' % (available_reg_index + 3, label_flag))
        #         if (ass_list.get(i).get(4).equals(<target_object>)){
        for i in range(len(res_info.get_identity())):
            new_sentences.append('    sget-object v%d, L' % (available_reg_index + 4) + res_info.get_func_path()[:-6] + ';->' + res_info.get_identity()[i] + '\n')
            new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
            new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
            new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
            new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
            new_sentences.append('    check-cast v%d, Ljava/util/List;\n' % (available_reg_index + 3))
            new_sentences.append('    const/16 v%d, 0x%d\n' % (available_reg_index + 5, (4 + i)))
            new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 3))
            new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 5))
            new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
            new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
            new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z\n' % (available_reg_index + 3, available_reg_index + 4))
            new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
            new_sentences.append('    if-eqz v%d, :relfix_%d_cond_1\n' % (available_reg_index + 3, label_flag))
        #             ass_list.remove(i);
        new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
        new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
        new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->remove(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
        #             Log.i("RelFix_release", "<release_func>");
        new_sentences.append('    const-string v%d, \"RelFix_release\"\n' % (available_reg_index + 6))
        new_sentences.append('    const-string v%d, \"%s\"\n' % (available_reg_index + 7, res_info.get_release_func()))
        new_sentences.append('    invoke-static/range {v%d .. v%d}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I\n' % (available_reg_index + 6, available_reg_index + 7))
        #         }
        #     }
        new_sentences.append('    :relfix_%d_cond_1\n' % label_flag)
        new_sentences.append('    add-int/lit8 v%d, v%d, 0x1\n' % (available_reg_index + 1, available_reg_index + 1))
        new_sentences.append('    goto :relfix_%d_goto_0\n' % label_flag)
        # }
        new_sentences.append('    :relfix_%d_cond_0\n' % label_flag)
        new_sentences.append('    .end local v%d    # \"i\":I\n' % (available_reg_index + 1))
        new_sentences.append('\n')

        contents[index:index] = new_sentences
        new_line_num += len(res_info.get_identity()) * 14 + 36
        index += new_line_num

    return return_num

