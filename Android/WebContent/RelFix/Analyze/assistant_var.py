#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Oct 13st, 2015
# Description: Add a global assistant list to help us release resources.
#

import os

from constant import *
from track_reg import *

##
# function: Insert new sentences in static constructor of main activity class file.
# @param contents: The original file contents
# @param index: The position of the new sentences
# @param main_act: The main activity
# @param flag: The flag of if we find a <clinit> method
#
def insert_static_cons(contents, index, main_act, flag):
    new_contents = []

    if 0 == flag:
        new_contents.append('\n')
        new_contents.append('.method static constructor <clinit>()V\n')
        new_contents.append('    .locals 1\n')
        new_contents.append('\n')
        new_contents.append('    .prologue')

    new_contents.append('\n')
    new_contents.append('    new-instance v0, Ljava/util/ArrayList;\n')
    new_contents.append('\n')
    new_contents.append('    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V\n')
    new_contents.append('\n')
    new_contents.append('    sput-object v0, L' + main_act + ';->' + Constants._ass_list_name + ':Ljava/util/List;\n')
    new_contents.append('\n')


    if 0 == flag:
        new_contents.append('    return-void\n')
        new_contents.append('.end method\n')
        
    if 0 == flag:
        contents += new_contents
    else:
        contents[index:index] = new_contents

##
# function: Add global assistant variables.
# @param smali_folder: The smali folder path
# @param main_act: The main activity
#
def add_ass_var(smali_folder, main_act):
    main_act_file = open(smali_folder + os.path.sep + main_act + '.smali', 'r')
    try:
        file_contents = main_act_file.readlines()
    finally:
        main_act_file.close()

    new_contents = []
    new_contents.append('\n')
    new_contents.append('.field public static ' + Constants._ass_list_name + ':Ljava/util/List;\n')
    new_contents.append('\n')
    new_contents.append('.field public static ' + Constants._ass_act_manager_name + ':Landroid/app/ActivityManager;\n')
    
    file_contents += new_contents

    # Add resource list.
    if '.method static constructor <clinit>()V\n' in file_contents:
        regs_index = file_contents.index('.method static constructor <clinit>()V\n')
        while file_contents[regs_index].find('.locals') < 0:
            regs_index += 1
        
        regs_num = file_contents[regs_index].strip(' \n').split(' ')[1]
        if '0' == regs_num:
            file_contents[regs_index] == '    .locals 1\n'

        return_index = file_contents.index('.method static constructor <clinit>()V\n')
        while file_contents[return_index].find('return-void') < 0:
            return_index += 1

        insert_static_cons(file_contents, return_index, main_act, 1)
    else:
        insert_static_cons(file_contents, 0, main_act, 0)

    # Add activity manager.
    for index, each_line in enumerate(file_contents):
        if each_line.find('invoke-super') >= 0 and each_line.find('onCreate(Landroid/os/Bundle;)V') >= 0:
            new_sentences = []
            new_sentences.append('\n')
            new_sentences.append('    const-string v0, \"activity\"\n')
            new_sentences.append('    invoke-virtual {p0, v0}, L' + main_act + ';->getSystemService(Ljava/lang/String;)Ljava/lang/Object;\n')
            new_sentences.append('    move-result-object v0\n')
            new_sentences.append('    check-cast v0, Landroid/app/ActivityManager;\n')
            new_sentences.append('    sput-object v0, L' + main_act + ';->' + Constants._ass_act_manager_name + ':Landroid/app/ActivityManager;\n')
            new_sentences.append('\n')

            file_contents[index+1:index+1] = new_sentences
            break

    main_act_file = open(smali_folder + os.path.sep + main_act + '.smali', 'w')
    try:
        main_act_file.writelines(file_contents)
    finally:
        main_act_file.close()
