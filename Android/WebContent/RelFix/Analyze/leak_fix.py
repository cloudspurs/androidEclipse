#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Oct 23st, 2015
# Description: Insert the release operations to fix the resource leak.
#

import os

from dynamic_judge import *

##
# Class: An activity or a service which need to be inserted with some release operations.
#
class component_need_fix: 
    ##
    # function: Constructor.
    # @param component_name: The activity or service name
    #
    def __init__(self, component_name):
        self.__component_name = component_name
        self.__resource_list = []
    
    ##
    # function: Insert a resource in a specific positon.
    # @param index: The position
    # @param leaked_res: The resource will be inserted
    #
    def insert_res(self, index, leaked_res):
        self.__resource_list.insert(index, leaked_res)

    ##
    # function: Append a resource after the list.
    # @param leake_res: The resource will be appended
    #
    def append_res(self, leaked_res):
        self.__resource_list.append(leaked_res)

    ##
    # function: Get the activity or service name.
    # @return: The component name
    #
    def get_component_name(self):
        return self.__component_name

    ##
    # function: Get the resource list.
    # @return: The resource list
    #
    def get_res_list(self):
        return self.__resource_list

##
# function: Insert the release operations in a specific place.
# @param contents: The smali file contents
# @param component: Resources need to be release in this component
# @param main_act: The main activity
# @param index: The position
# @param flag: The flag of life-cycle callbacks
#
def insert_release_op(contents, component, main_act, index, flag):
    lifecycle = ['onPause()', 'onStop()', 'onDestroy()']

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

    new_sentences = []
    new_sen_num = 0

    new_sentences.append('\n')
    # for (int i = ass_list.size() - 1; i >= 0; i--){
    new_sentences.append('    sget-object v%d, L' % (available_reg_index + 2) + main_act + ';->' + Constants._ass_list_name + ':Ljava/util/List;\n')
    new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->size()I\n' % (available_reg_index + 2, available_reg_index + 2))
    new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
    new_sentences.append('    const/16 v%d, 0x1\n' % (available_reg_index + 1))
    new_sentences.append('    sub-int v%d, v%d, v%d\n' % (available_reg_index + 1, available_reg_index + 3, available_reg_index + 1))
    new_sentences.append('    .local v%d, \"i\":I\n' % (available_reg_index + 1))
    new_sentences.append('    :relfix_%d_goto_0\n' % label_flag)
    new_sentences.append('    if-ltz v%d, :relfix_%d_cond_0\n' % (available_reg_index + 1, label_flag))
    #     if (ass_list.get(i).get(2).equals(<component_name>)){
    new_sentences.append('    const-string v%d, \"' % (available_reg_index + 4) + component.get_component_name().replace(os.path.sep, '.')[1:-1] + '\"\n')
    new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
    new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
    new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
    new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
    new_sentences.append('    check-cast v%d, Ljava/util/List;\n' % (available_reg_index + 3))
    new_sentences.append('    const/16 v%d, 0x2\n' % (available_reg_index + 5))
    new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 3))
    new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 5))
    new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
    new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
    new_sentences.append('    check-cast v%d, Ljava/lang/String;\n' % (available_reg_index + 3))
    new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z\n' % (available_reg_index + 3, available_reg_index + 4))
    new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
    new_sentences.append('    if-eqz v%d, :relfix_%d_cond_1\n' % (available_reg_index + 3, label_flag))

    new_sen_num += 24

    #         if (ass_list.get(i).get(0).equals(<apply_func>)){
    res_list = component.get_res_list()
    cond_flag = 2
    is_first = True
    for i in range(len(res_list)):
        if lifecycle[flag] == res_list[i].get_suggested_rel_place():
            if not is_first:
                new_sentences.append('    :relfix_%d_cond_%d\n' % (label_flag, cond_flag))

                cond_flag += 1
                new_sen_num += 1
            
            is_first = False

            new_sentences.append('    const-string v%d, \"' % (available_reg_index + 4) + res_list[i].get_apply_func() + '\"\n')
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

            is_last = True
            for j in range(i + 1, len(res_list)):
                if lifecycle[flag] == res_list[j].get_suggested_rel_place():
                    is_last = False

            if is_last:
                new_sentences.append('    if-eqz v%d, :relfix_%d_cond_1\n' % (available_reg_index + 3, label_flag))
            else:
                new_sentences.append('    if-eqz v%d, :relfix_%d_cond_%d\n' % (available_reg_index + 3, label_flag, cond_flag))

            new_sen_num += 15

    #             <release_op>
            for j in range(len(res_list[i].get_identity())):
                new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
                new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
                new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
                new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
                new_sentences.append('    check-cast v%d, Ljava/util/List;\n' % (available_reg_index + 3))
                new_sentences.append('    const/16 v%d, 0x%d\n' % (available_reg_index + 5, (4 + j)))
                new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 3))
                new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 5))
                new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
                new_sentences.append('    move-result-object v%d\n' % (available_reg_index + (8 + j)))
                new_sentences.append('    check-cast v%d, ' % (available_reg_index + (8 + j)) + res_list[i].get_identity()[j].split(':')[1] + '\n')

                new_sen_num += 11

            new_sentences.append('    invoke-virtual/range {v%d .. v%d}, ' % (available_reg_index + 8, available_reg_index + (8 + len(res_list[i].get_identity()) - 1)) + res_list[i].get_rel_func() + '\n')
    #             ass_list.remove(i);
            new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
            new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
            new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->remove(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
    #             Log.i("RelFix_fix", "<release_func>");
            new_sentences.append('    const-string v%d, \"RelFix_fix\"\n' % (available_reg_index + 6))
            new_sentences.append('    const-string v%d, \"%s\"\n' % (available_reg_index + 7, res_list[i].get_rel_func()))
            new_sentences.append('    invoke-static/range {v%d .. v%d}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I\n' % (available_reg_index + 6, available_reg_index + 7))
            new_sentences.append('    goto :relfix_%d_goto_1\n' % (label_flag))

            new_sen_num += 8
    #         }
    #     }
    new_sentences.append('    :relfix_%d_cond_1\n' % (label_flag))
    new_sentences.append('    :relfix_%d_goto_1\n' % (label_flag))
    new_sentences.append('    const/16 v%d, 0x1\n' % (available_reg_index))
    new_sentences.append('    sub-int v%d, v%d, v%d\n' % (available_reg_index + 1, available_reg_index + 1, available_reg_index))
    new_sentences.append('    goto :relfix_%d_goto_0\n' % (label_flag))
    # }
    new_sentences.append('    :relfix_%d_cond_0\n' % label_flag)
    new_sentences.append('    .end local v%d    # \"i\":I\n' % (available_reg_index + 1))
    new_sentences.append('\n')

    new_sen_num += 8

    contents[index:index] = new_sentences
    index += new_sen_num

##
# function: Insert the release operations.
# @param all_leaked_res: All leaked resources information
# @param main_act: The main activity
# @param act_list: All activities
# @param smali_folder: The smali folder path
# @param act_redir_dic: The activity redirection info
#
def add_release_op(all_leaked_res, main_act, act_list, smali_folder, act_redir_dic):
    component_list = []

    for res in all_leaked_res:
        for tracked_component in res.get_trace_func():
            if 3 == tracked_component[1]:
                new_list = []
                for each_act in act_list:
                    new_list.append(['L' + each_act + ';', 1])
                res.set_trace_func(new_list)
        for tracked_component in res.get_trace_func():
            component_exist = False
            for component in component_list:
                if tracked_component[0] == component.get_component_name():
                    component_exist = True
                    component.append_res(res)

            if False == component_exist:
                new_component = component_need_fix(tracked_component[0])
                new_component.append_res(res)
                component_list.append(new_component)

    for each_com in component_list:
        smali_file = open(smali_folder + os.path.sep + act_redir_dic[each_com.get_component_name()][1:-1] + '.smali', 'r')

        try:
            smali_contents = smali_file.readlines()
        finally:
            smali_file.close()

        need_pause = False
        need_stop = False
        need_destroy = False
        for each_res in each_com.get_res_list():
            if each_res.get_suggested_rel_place().find('onPause') >= 0:
                need_pause = True
            elif each_res.get_suggested_rel_place().find('onStop') >= 0:
                need_stop = True
            elif each_res.get_suggested_rel_place().find('onDestroy') >= 0:
                need_destroy = True
        
        if True == need_pause:
            find_onpause = False
            for index, each_line in enumerate(smali_contents):
                if each_line.find('.method') >= 0 and each_line.find('onPause()V') >= 0:
                    pause_index = index
                    find_onpause = True

                    while smali_contents[pause_index].find('return-void') < 0 and smali_contents[pause_index].find('java/lang/System;->exit(I)V') < 0:
                        pause_index += 1

                    insert_release_op(smali_contents, each_com, main_act, pause_index, 0)
            if False == find_onpause:
                new_sentences = []

                new_sentences.append('\n')
                new_sentences.append('.method protected onPause()V\n')
                new_sentences.append('    .locals 0\n')
                new_sentences.append('\n')
                new_sentences.append('    .prologue\n')
                new_sentences.append('    invoke-super {v0}, Landroid/app/Activity;->onPause()V\n')
                new_sentences.append('\n')
                new_sentences.append('    return-void\n')
                new_sentences.append('.end method\n')
                new_sentences.append('\n')

                smali_contents += new_sentences

                for index, each_line in enumerate(smali_contents):
                    if each_line.find('.method protected onPause()V') >= 0:
                        pause_index = index
                        find_onpause = True

                        while smali_contents[pause_index].find('return-void') < 0:
                            pause_index += 1

                        insert_release_op(smali_contents, each_com, main_act, pause_index, 0)

        if True == need_stop:
            find_onstop = False
            for index, each_line in enumerate(smali_contents):
                if each_line.find('.method') >= 0 and each_line.find('onStop()V') >= 0:
                    stop_index = index
                    find_onstop = True

                    while smali_contents[stop_index].find('return-void') < 0 and smali_contents[stop_index].find('java/lang/System;->exit(I)V') < 0:
                        stop_index += 1

                    insert_release_op(smali_contents, each_com, main_act, stop_index, 1)
            if False == find_onstop:
                new_sentences = []

                new_sentences.append('\n')
                new_sentences.append('.method protected onStop()V\n')
                new_sentences.append('    .locals 0\n')
                new_sentences.append('\n')
                new_sentences.append('    .prologue\n')
                new_sentences.append('    invoke-super {v0}, Landroid/app/Activity;->onStop()V\n')
                new_sentences.append('\n')
                new_sentences.append('    return-void\n')
                new_sentences.append('.end method\n')
                new_sentences.append('\n')

                smali_contents += new_sentences

                for index, each_line in enumerate(smali_contents):
                    if each_line.find('.method protected onStop()V') >= 0:
                        stop_index = index
                        find_onstop = True

                        while smali_contents[stop_index].find('return-void') < 0:
                            stop_index += 1

                        insert_release_op(smali_contents, each_com, main_act, pause_index, 1)

        if True == need_destroy:
            find_ondestroy = False
            for index, each_line in enumerate(smali_contents):
                if each_line.find('.method') >= 0 and each_line.find('onDestroy()V') >= 0:
                    destroy_index = index
                    find_ondestroy = True

                    while smali_contents[destroy_index].find('return-void') < 0 and smali_contents[destroy_index].find('java/lang/System;->exit(I)V') < 0:
                        destroy_index += 1

                    insert_release_op(smali_contents, each_com, main_act, destroy_index, 2)
            if False == find_ondestroy:
                new_sentences = []

                new_sentences.append('\n')
                new_sentences.append('.method protected onDestroy()V\n')
                new_sentences.append('    .locals 0\n')
                new_sentences.append('\n')
                new_sentences.append('    .prologue\n')
                new_sentences.append('    invoke-super {v0}, Landroid/app/Activity;->onDestroy()V\n')
                new_sentences.append('\n')
                new_sentences.append('    return-void\n')
                new_sentences.append('.end method\n')
                new_sentences.append('\n')

                smali_contents += new_sentences

                for index, each_line in enumerate(smali_contents):
                    if each_line.find('.method protected onDestroy()V') >= 0:
                        destroy_index = index
                        find_ondestroy = True

                        while smali_contents[destroy_index].find('return-void') < 0:
                            destroy_index += 1

                        insert_release_op(smali_contents, each_com, main_act, destroy_index, 2)
        
        smali_file = open(smali_folder + os.path.sep + act_redir_dic[each_com.get_component_name()][1:-1] + '.smali', 'w')

        try:
            smali_file.writelines(smali_contents)
        finally:
            smali_file.close()

##
# function: Add release operations before a specific release operation.
# @param contents: The smali file contents
# @param index: The place where insert the sentences
# @param all_res: All leaked resources
# @param main_act: The main activity
# @param res_info: The resource information
# @param res_type: The typu of the operation
#
def add_special_release_op(contents, index, all_res, main_act, res_info, res_type):
    if 'RelInfo' == res_type:
        for each_res in all_res:
            if each_res.get_rel_func().find(res_info.get_release_func()) >= 0:
                priority = int(each_res.get_priority())
                if not 0 == priority:
                    temp_pri = priority - 1
                    while temp_pri > 0:
                        for other_res in all_res:
                            if other_res.get_apply_func().split('->')[0] == each_res.get_apply_func().split('->')[0] and int(other_res.get_priority()) == temp_pri:
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

                                new_sentences = []

                                new_sentences.append('\n')
                                # for (int i = ass_list.size() - 1; i >= 0; i--){
                                new_sentences.append('    sget-object v%d, L' % (available_reg_index + 2) + main_act + ';->' + Constants._ass_list_name + ':Ljava/util/List;\n')
                                new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->size()I\n' % (available_reg_index + 2, available_reg_index + 2))
                                new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
                                new_sentences.append('    const/16 v%d, 0x1\n' % (available_reg_index + 1))
                                new_sentences.append('    sub-int v%d, v%d, v%d\n' % (available_reg_index + 1, available_reg_index + 3, available_reg_index + 1))
                                new_sentences.append('    .local v%d, \"i\":I\n' % (available_reg_index + 1))
                                new_sentences.append('    :relfix_%d_goto_0\n' % label_flag)
                                new_sentences.append('    if-ltz v%d, :relfix_%d_cond_0\n' % (available_reg_index + 1, label_flag))
                                #     if (ass_list.get(i).get(0).equals(<apply_func>)){
                                new_sentences.append('    const-string v%d, \"' % (available_reg_index + 4) + other_res.get_apply_func() + '\"\n')
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
                                #         if (ass_list.get(i).get(4).equals(<resource_object>)){
                                new_sentences.append('    sget-object v%d, L' % (available_reg_index + 4) + other_res.get_func_path()[:-6] + ';->' + other_res.get_identity()[0] + '\n')
                                new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
                                new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
                                new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
                                new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
                                new_sentences.append('    check-cast v%d, Ljava/util/List;\n' % (available_reg_index + 3))
                                new_sentences.append('    const/16 v%d, 0x4\n' % (available_reg_index + 5))
                                new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 3))
                                new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 5))
                                new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
                                new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
                                new_sentences.append('    invoke-virtual/range {v%d .. v%d}, Ljava/lang/Object;->equals(Ljava/lang/Object;)Z\n' % (available_reg_index + 3, available_reg_index + 4))
                                new_sentences.append('    move-result v%d\n' % (available_reg_index + 3))
                                new_sentences.append('    if-eqz v%d, :relfix_%d_cond_1\n' % (available_reg_index + 3, label_flag))

                                #             <release_op>
                                for j in range(len(other_res.get_identity())):
                                    new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
                                    new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
                                    new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
                                    new_sentences.append('    move-result-object v%d\n' % (available_reg_index + 3))
                                    new_sentences.append('    check-cast v%d, Ljava/util/List;\n' % (available_reg_index + 3))
                                    new_sentences.append('    const/16 v%d, 0x%d\n' % (available_reg_index + 5, (4 + j)))
                                    new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 3))
                                    new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 5))
                                    new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->get(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
                                    new_sentences.append('    move-result-object v%d\n' % (available_reg_index + (8 + j)))
                                    new_sentences.append('    check-cast v%d, ' % (available_reg_index + (8 + j)) + other_res.get_identity()[j].split(':')[1] + '\n')

                                new_sentences.append('    invoke-virtual/range {v%d .. v%d}, ' % (available_reg_index + 8, available_reg_index + (8 + len(other_res.get_identity()) - 1)) + other_res.get_rel_func() + '\n')
                                #             ass_list.remove(i);
                                new_sentences.append('    move-object/16 v%d, v%d\n' % (available_reg_index + 6, available_reg_index + 2))
                                new_sentences.append('    move/16 v%d, v%d\n' % (available_reg_index + 7, available_reg_index + 1))
                                new_sentences.append('    invoke-interface/range {v%d .. v%d}, Ljava/util/List;->remove(I)Ljava/lang/Object;\n' % (available_reg_index + 6, available_reg_index + 7))
                                #             Log.i("RelFix_fix", "<release_func>");
                                new_sentences.append('    const-string v%d, \"RelFix_fix\"\n' % (available_reg_index + 6))
                                new_sentences.append('    const-string v%d, \"%s\"\n' % (available_reg_index + 7, other_res.get_rel_func()))
                                new_sentences.append('    invoke-static/range {v%d .. v%d}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I\n' % (available_reg_index + 6, available_reg_index + 7))
                                #         }
                                #     }
                                new_sentences.append('    :relfix_%d_cond_1\n' % label_flag)
                                new_sentences.append('    const/16 v%d, 0x1\n' % (available_reg_index))
                                new_sentences.append('    sub-int v%d, v%d, v%d\n' % (available_reg_index + 1, available_reg_index + 1, available_reg_index))
                                new_sentences.append('    goto :relfix_%d_goto_0\n' % label_flag)
                                # }
                                new_sentences.append('    :relfix_%d_cond_0\n' % label_flag)
                                new_sentences.append('    .end local v%d    # \"i\":I\n' % (available_reg_index + 1))
                                new_sentences.append('\n')

                                contents[index:index] = new_sentences
                                break
                         
                        temp_pri -= 1


