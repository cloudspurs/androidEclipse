#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Aug 21st, 2015
# Description: Main file for resource leak fixing.
#

import os
import sys
import datetime
from optparse import OptionParser

sys.path.append('.' + os.path.sep)

from Analyze.FCG import *
from Analyze.leaked_res import *
from Analyze.info_table import *
from Analyze.constant import *
from Analyze.track_reg import *
from Analyze.track_act import *
from Analyze.handle_async import *
from Analyze.rel_info import *
from Analyze.parse_manifest import *
from Analyze.assistant_var import *
from Analyze.leak_fix import *
from Analyze.inhe_graph import *
from Analyze.redir_act import *

def gen_option_parser():
    usage = 'RelFix.py [options] apk_file'
    parser = OptionParser(usage)

    parser.add_option('-p', '--preserve', action='store_true', dest='is_preserve', default=False,
            help='Preserve the decompiled files.')

    return parser

if '__main__' == __name__:
    opt_parser = gen_option_parser()
    (options, args) = opt_parser.parse_args()

    # Some path informations.
    apk_file_path = os.path.abspath(args[0])
    parent_folder = os.path.abspath(os.path.join(apk_file_path, os.pardir))
    app_name = apk_file_path.strip(' \n').split(os.path.sep)[-1][:-4]
    new_apk_name = app_name + '_fixed'
    log_file_path = parent_folder + os.path.sep + Constants._log_file_name

    if not os.path.exists(log_file_path):
        print('---> Need a \'log_info\' file')
        sys.exit()

    apktool_target_folder = parent_folder + os.path.sep + app_name + '_apktool'
    dist_folder = apktool_target_folder + os.path.sep + 'dist'
    smali_folder = apktool_target_folder + os.path.sep + 'smali'
    manifest_path = apktool_target_folder + os.path.sep + Constants._manifest_file_name

    # Unpack the apk file using Apktool.
    apktool_decompile_command = Constants._apktool + ' d -f ' + apk_file_path + ' -o ' + apktool_target_folder

    if 0 == os.system(apktool_decompile_command):
        print('---> Decompile complete\n')
    else:
        print('---> Decompile failed\n')
        sys.exit()

    # Get informations of the main activity.
    main_act = ManifestParser(manifest_path).get_main_act()
    act_list = ManifestParser(manifest_path).get_all_act()
    act_list = check_act(act_list, smali_folder)
    act_redir_dic = redirect_act(act_list, smali_folder)

    # Test.
    #print('--> act_list')
    #for each_act in act_list:
    #    print(each_act)
    #print('')

    # Build inheritance graph.
    inhe_graph = InheGraph(smali_folder).get_graph()
        
    # Construct FCG and aFCG.
    time_start = datetime.datetime.now()
    apkFCG = FCG(smali_folder, inhe_graph).get_FCG()
    apkrFCG = FCG(smali_folder, inhe_graph).get_rFCG()
    apkaFCG = AsyncGraph(apkrFCG, act_list, smali_folder).get_aFCG()
    apkraFCG = AsyncGraph(apkrFCG, act_list, smali_folder).get_raFCG()
    time_end = datetime.datetime.now()
    graph_time = time_end - time_start

    # Test.
    #print('--> raFCG')
    #for listener in apkraFCG:
    #    print(listener + ':')
    #    for registration in apkraFCG[listener]:
    #        print(registration)
    #    print('')
    #print('')

    time_start = datetime.datetime.now()
    # Add global assistant variables.
    add_ass_var(smali_folder, main_act)

    # Modify manifest file.
    modify_manifest(manifest_path)

    # Find the leaked rerources from 'log_info' file.
    log_info_file = open(log_file_path, 'r')
    try:
        log_info_contents = log_info_file.readlines()
    finally:
        log_info_file.close()

    all_leaked_res = []

    for log_index, each_line_content in enumerate(log_info_contents):
        if each_line_content.find('applying sentence log') >= 0:
            func_path = log_info_contents[log_index + 1].split(':')[1].strip('\n').strip(' ')
            func_name = log_info_contents[log_index + 2].split(':')[1].strip('\n').strip(' ')
            apply_method = log_info_contents[log_index + 3].split(':')[1].strip('\n').strip(' ')

            new_leaked_res = LeakedRes(func_path, func_name, apply_method)
            all_leaked_res.append(new_leaked_res)

    # Find the activity a resrouce may be released in.
    track_activity(all_leaked_res, apkrFCG, apkraFCG, act_list)

    # Track registers the applying method uses.
    for res_index, each_leaked_res in enumerate(all_leaked_res):
        if res_index > 0 and each_leaked_res.get_func_path() == all_leaked_res[res_index - 1].get_func_path() \
                and each_leaked_res.get_func_name() == all_leaked_res[res_index - 1].get_func_name() \
                and each_leaked_res.get_apply_func() == all_leaked_res[res_index - 1].get_apply_func():
                    flag += 1
        else:
            flag = 1

        track_registers(smali_folder, all_leaked_res, each_leaked_res, flag, 'LeakedRes', main_act)

    all_rel_op = []

    for log_index, each_line_content in enumerate(log_info_contents):
        if each_line_content.find('release sentence log') >= 0:
            func_path = log_info_contents[log_index + 1].split(':')[1].strip('\n').strip(' ')
            func_name = log_info_contents[log_index + 2].split(':')[1].strip('\n').strip(' ')
            release_method = log_info_contents[log_index + 3].split(':')[1].strip('\n').strip(' ')

            new_rel_op = RelInfo(func_path, func_name, release_method)
            all_rel_op.append(new_rel_op)

    # Track registers the release method uses.
    for res_index, each_rel_op in enumerate(all_rel_op):
        if res_index > 0 and each_rel_op.get_func_path() == all_rel_op[res_index - 1].get_func_path() \
                and each_rel_op.get_func_name() == all_rel_op[res_index - 1].get_func_name() \
                and each_rel_op.get_release_func() == all_rel_op[res_index - 1].get_release_func():
                    flag += 1
        else:
            flag = 1

        track_registers(smali_folder, all_leaked_res, each_rel_op, flag, 'RelInfo', main_act)
    
    print('--> Potential leaked resource request operations <--')
    for each_res in all_leaked_res:
        print('-operation: ' + each_res.get_apply_func())
        print('-file: ' + each_res.get_func_path())
        print('-method: ' + each_res.get_func_name())
        #print(each_res.get_identity())
        print('-CRO: ' + each_res.get_rel_func())
        print('-release method: ' + each_res.get_suggested_rel_place())
        #print(each_res.get_arg_from())
        #print(each_res.get_priority())
        #print(each_res.get_trace_func())
        print('')
    print('')

    print('--> Related resource release operations <--')
    for each_rel_op in all_rel_op:
        print('-operation: ' + each_rel_op.get_release_func())
        print('-file: ' + each_rel_op.get_func_path())
        print('-method: ' + each_rel_op.get_func_name())
        #print(each_rel_op.get_identity())
        print('')
    print('')

    # Insert the release operations.
    add_release_op(all_leaked_res, main_act, act_list, smali_folder, act_redir_dic)
    time_end = datetime.datetime.now()
    fix_time = time_end - time_start

    # Repack all files to apk and sign the repacked apk.
    apktool_build_command = Constants._apktool + ' b ' + apktool_target_folder

    if 0 == os.system(apktool_build_command):
        print('---> Rebuild project to Apk file complete\n')
    else:
        print('---> Rebuild failed\n')
        sys.exit()

    sign_command = 'java -jar ' + Constants._signapk_file + ' ' + Constants._pem_file + ' ' + Constants._pk8_file + ' ' + dist_folder + os.path.sep + app_name + '.apk ' + dist_folder + os.path.sep + new_apk_name + '.apk' 
    if 0 == os.system(sign_command):
        print('---> Sign Apk complete\n')
    else:
        print('---> Sign Apk failed\n')

    copy_command = 'cp ' + dist_folder + os.path.sep + new_apk_name + '.apk ' + parent_folder
    if 0 == os.system(copy_command):
        print('---> Copy file complete\n')
        print('-----------------> ALL DONE <-----------------')
        print('---> Graph Build time: ' + str(graph_time.microseconds / 1000) + 'ms')
        print('---> Leak Fix time: ' + str(fix_time.microseconds / 1000) + 'ms')
        print('---> Total time: ' + str(fix_time.microseconds / 1000 + graph_time.microseconds / 1000) + 'ms')
    else:
        print('---> Copy file failed\n')

    if not options.is_preserve and os.path.exists(apktool_target_folder):
        os.system('rm -rf ' + apktool_target_folder)
