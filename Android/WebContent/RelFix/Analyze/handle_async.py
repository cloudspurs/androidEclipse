#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Oct 8th, 2015
# Description: Handle asynchronous callbacks.
#

import os
import re

from track_reg import *
from constant import *
from track_act import *

##
# Class: Scan smali files to build a graph for handling asynchronous callbacks.
#
class AsyncGraph(object):
    ##
    # function: Constructor.
    # @param rfcg: The rFCG
    # @param act_list: All activities in the app
    # @param smali_folder: The Smali folder path
    #
    def __init__(self, rfcg, act_list, smali_folder):
        if not hasattr(self, '_AsyncGraph__afcg'):
            self.__rfcg = rfcg
            self.__act_list = act_list
            self.__smali_folder = smali_folder
            self.__afcg = {}
            self.__rafcg = {}
            self.__thread_list = []

            self.__find_thread('')

            self.__done = False
            while not self.__done:
                self.__done = True
                self.__obtain_afcg('')

    ##
    # function: This method for creating a Singleton.
    #
    def __new__(cls, rfcg, act_list, smali_folder):
        if not hasattr(cls, 'instance'):
            cls.instance = object.__new__(cls, rfcg, act_list, smali_folder)

        return cls.instance

    ##
    # function: Obtain the aFCG from scaning smali files for handling asynchronous callbacks.
    # @param file_path: The target file path
    #
    def __obtain_afcg(self, file_path):
        # Don't scan the Android package
        if 'android' == file_path:
            return

        if '' == file_path:
            target_path = self.__smali_folder
        else:
            target_path = self.__smali_folder + os.path.sep + file_path

        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                for item in os.listdir(target_path):
                    if '' == file_path:
                        self.__obtain_afcg(item)
                    else:
                        self.__obtain_afcg(file_path + os.path.sep + item)
            else:
                # Get each lines of the smali file
                smali_file = open(target_path, 'r')
                file_contents = []
                try:
                    file_contents = smali_file.readlines()
                finally:
                    smali_file.close()

                for index, each_line in enumerate(file_contents):
                    find_registration = False

                    # setOnClickListener(
                    if each_line.find('setOnClickListener(') >= 0 and each_line.find('Landroid/') >= 0 and each_line.find('invoke') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            #caller_reg = each_line.split('{')[1].split('}')[0].split(',')[0].strip(' ')
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[1].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            #caller_reg = base_reg
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 1)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onClick(Landroid/view/View;)V'
                        #component = self.__track_reg_find_class(file_contents, index, caller_reg)
                        component = self.__FCG_find_class(file_contents, index, listener)
                    # Landroid/hardware/Camera;->takePicture(
                    elif each_line.find('Landroid/hardware/Camera;->takePicture(') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[3].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 3)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onPictureTaken([BLandroid/hardware/Camera;)V'
                        component = self.__FCG_find_class(file_contents, index, listener)
                    # Landroid/hardware/SensorManager;->registerListener(
                    elif each_line.find('Landroid/hardware/SensorManager;->registerListener(') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[1].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 1)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onSensorChanged(Landroid/hardware/SensorEvent;)V'
                        component = self.__FCG_find_class(file_contents, index, listener)
                    elif each_line.find('Landroid/location/LocationManager;->requestLocationUpdates(') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[5].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 5)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onLocationChanged(Landroid/location/Location;)V'
                        component = self.__FCG_find_class(file_contents, index, listener)
                    elif each_line.find(';->bindService(Landroid/content/Intent;') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[2].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 2)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onServiceConnected(Landroid/content/ComponentName;Landroid/os/IBinder;)V'
                        component = self.__FCG_find_class(file_contents, index, listener)
                    elif each_line.find(';->addOnGlobalLayoutListener(') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[1].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 1)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onGlobalLayout()V'
                        component = self.__FCG_find_class(file_contents, index, listener)
                    elif each_line.find('Landroid/media/MediaPlayer;->setOnCompletionListener(') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[1].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 1)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onCompletion(Landroid/media/MediaPlayer;)V'
                        component = self.__FCG_find_class(file_contents, index, listener)
                    elif each_line.find('Landroid/media/MediaPlayer;->setOnPreparedListener(') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[1].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 1)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onPrepared(Landroid/media/MediaPlayer;)V'
                        component = self.__FCG_find_class(file_contents, index, listener)
                    elif each_line.find('Landroid/media/MediaPlayer;->setOnErrorListener(') >= 0:
                        find_registration = True

                        if each_line.find('/range') < 0:
                            listener_reg = each_line.split('{')[1].split('}')[0].split(',')[1].strip(' ')
                        else:
                            base_reg = each_line.split('{')[1].split('}')[0].split('..')[0].strip(' ')
                            listener_reg = base_reg[0] + str(int(base_reg[1:]) + 1)
                        listener = self.__track_reg_find_class(file_contents, index, listener_reg)
                        if not 0 == len(listener):
                            for i, each in enumerate(listener):
                                listener[i] = listener[i] + '->onError(Landroid/media/MediaPlayer;II)Z'
                        component = self.__FCG_find_class(file_contents, index, listener)

                    if find_registration and not 0 == len(component) and not 0 == len(listener):
                        for each_com in component:
                            if not each_com in self.__afcg:
                                self.__afcg[each_com] = []
                            for each_lis in listener:
                                if not each_lis in self.__rafcg:
                                    self.__rafcg[each_lis] = []
                                if not each_lis in self.__afcg[each_com]:
                                    self.__done = False
                                    self.__afcg[each_com].append(each_lis)
                                if not each_com in self.__rafcg[each_lis]:
                                    self.__done = False
                                    self.__rafcg[each_lis].append(each_com)

    ##
    # function: Find the activity class by using FCG.
    # @param contents: The smali file contents
    # @param index: The current index of the contents
    # @param listener: The listener callback method
    # @return: The class's type
    #
    def __FCG_find_class(self, contents, index, listener):
        while contents[index].find('.method') < 0:
            index -= 1

        func_name = contents[0].strip(' \n').split(' ')[-1] + '->' + contents[index].strip(' \n').split(' ')[-1]
        track_list = [[func_name, 0]]
        trash_list = []
        while need_more_track(track_list, self.__act_list):
            for i, each in enumerate(track_list):
                for each_lis in listener:
                    if each_lis == each[0]:
                        trash_list.append(track_list[i][0])
                        del(track_list[i])
                        i -= 1

            i = 0
            while i < len(track_list):
                if 0 == track_list[i][1]:
                    if 0 == len(self.__rfcg[track_list[i][0]]):
                        if track_list[i][0] in self.__rafcg:
                            for item in self.__rafcg[track_list[i][0]]:
                                if not [item, 1] in track_list:
                                    track_list.append([item, 1])
                            trash_list.append(track_list[i][0])
                            del(track_list[i])
                            i -= 1
                        else:
                            track_list[i][1] = 3
                    else:
                        new_flag = False
                        for new_func in self.__rfcg[track_list[i][0]]:
                            if not [new_func, 2] in track_list and not new_func in trash_list:
                                track_list.append([new_func, 2])
                                new_flag = True
                        trash_list.append(track_list[i][0])
                        del(track_list[i])
                        i -= 1
                i += 1

            for each_func in track_list:
                if 2 == each_func[1]:
                    each_func[1] = 0

        result = []
        for each in track_list:
            if 1 == each[1]:
                result.append(each[0])

        return result
    
    ##
    # function: Track a field variable.
    # @param contents: The smali file contents
    # @param index: The current index of the contents
    # @param field: The variable name
    # @return: The variable's type
    #
    def __track_field(self, contents, index, field):
        index = next_valid_index(contents, index, 1)
        sen_split = re.split('[ ,{}]', contents[index].strip(' \n'))
        while '' in sen_split:
            sen_split.remove('')
        while (not field == sen_split[-1]) or contents[index].find('put-object') < 0:
            index = next_valid_index(contents, index, 1)
            if 0 == index:
                return []
            sen_split = re.split('[ ,{}]', contents[index].strip(' \n'))
            while '' in sen_split:
                sen_split.remove('')

        reg_name = sen_split[1]
        result = self.__track_reg_find_class(contents, index, reg_name)
        return result

    ##
    # function: Track method invoker.
    # @param contents: The smali file contents
    # @param index: The current index of the contents
    # @param reg: The register name
    # @return: The class's type
    #
    def __track_invoker(self, contents, index, reg):
        callee_method = contents[0].strip(' \n').split(' ')[-1] + '->' + contents[index].strip(' \n').split(' ')[-1]

        if not 0 == len(self.__rfcg[callee_method]):
            caller_methods = self.__rfcg[callee_method]
        else:
            return []

        result = []
        for caller_method in caller_methods:
            caller_method_path = caller_method.split(';->')[0].lstrip('L') + '.smali'
            caller_method_function = caller_method.split(';->')[1]

            caller_smali_file = open(self.__smali_folder + os.path.sep + caller_method_path, 'r')
            try:
                smali_contents = caller_smali_file.readlines()
            finally:
                caller_smali_file.close()

            for caller_index in range(len(smali_contents)):
                if smali_contents[caller_index].find(caller_method_function) >= 0 and smali_contents[caller_index].find('.method') >= 0:
                    temp_index = caller_index

                    while smali_contents[temp_index].find(callee_method) < 0 or smali_contents[temp_index].find('invoke') < 0:
                        temp_index += 1

                    if smali_contents[temp_index].find('/range') < 0:
                        track_reg = smali_contents[temp_index].split('{')[1].split('}')[0].split(',')[int(reg.strip('p'))].strip(' ')
                    else:
                        base_reg = smali_contents[temp_index].split('{')[1].split('}')[0].split('..')[0].strip(' ')
                        track_reg = base_reg[0] + str(int(base_reg[1:]) + int(reg.strip('p')))
                    result += self.__track_reg_find_class(smali_contents, temp_index, track_reg)
        return result

    ##
    # function: Find the activity and listener class by tracking registers.
    # @param contents: The smali file contents
    # @param index: The current index of the contents
    # @param reg: The register name
    # @return: The class's type
    #
    def __track_reg_find_class(self, contents, index, reg):
        result = []

        if reg.find('p') >= 0:
            method_index = index
            while contents[method_index].find('.method') < 0:
                method_index -= 1

            param_list = get_param_seq(contents[method_index].split('(')[1].split(')')[0])
            if contents[method_index].find('static') >= 0:
                reg_type = param_list[int(reg.strip('p'))]
            else:
                if 'p0' == reg:
                    reg_type = contents[0].strip(' \n').split(' ')[-1]
                else:
                    reg_type = param_list[int(reg.strip('p')) - 1]

            if reg_type.split('/')[0].find('android') >= 0:
                result = self.__track_invoker(contents, method_index, reg)
            else:
                result.append(reg_type)

        else: 
            index = next_valid_index(contents, index, 1)
            sen_split = re.split('[ ,{}]', contents[index].strip(' \n'))
            while '' in sen_split:
                sen_split.remove('')
            while '.' == sen_split[0][0] or sen_split[0].find('if-') >= 0 or sen_split[0].find('put-object') >= 0 or sen_split[0].find('check-cast') >= 0 or sen_split[0].find('invoke-') >= 0 or len(sen_split) < 2 or not reg == sen_split[1]:
                index = next_valid_index(contents, index, 1)
                sen_split = re.split('[ ,{}]', contents[index].strip(' \n'))
                while '' in sen_split:
                    sen_split.remove('')
               
            if contents[index].find('new-instance') >= 0:
                result.append(contents[index].strip(' \n').split(',')[-1].strip(' '))

            elif contents[index].find('get-object') >= 0:
                reg_type = contents[index].strip(' \n').split(':')[1]
                if reg_type.split('/')[0].find('android') >= 0:
                    field = contents[index].strip(' \n').split(' ')[-1]
                    result = self.__track_field(contents, index, field)
                else:
                    result.append(reg_type)

            elif contents[index].find('move-result-object') >= 0:
                index = next_valid_index(contents, index, 1)
                sen_split = re.split('[ ,{}]', contents[index].strip(' \n'))
                while '' in sen_split:
                    sen_split.remove('')
                target_class = sen_split[-1].split('->')[0]
                target_method = sen_split[-1].split('->')[1]
                if not os.path.exists(self.__smali_folder + os.path.sep + target_class[1:-1] + '.smali'):
                    print('---> WARNING: move-result-object => no such file: ' + self.__smali_folder + os.path.sep + target_class[1:-1] + '.smali')
                    return []

                target_file = open(self.__smali_folder + os.path.sep + target_class[1:-1] + '.smali', 'r')
                try:
                    target_contents = target_file.readlines()
                finally:
                    target_file.close()

                for index, each_line in enumerate(target_contents):
                    if each_line.find('.method') >= 0 and each_line.find(target_method) >= 0:
                        temp_index = index
                        while target_contents[temp_index].find('return') < 0:
                            temp_index = next_valid_index(target_contents, temp_index, 2)
                            if target_contents[temp_index].find('.end method') >= 0:
                                print('---> WARNING: move-result-object => no return operation: ' + contents[index])
                                return []

            elif contents[index].find('move-object') >= 0:
                sen_split = re.split('[ ,{}]', contents[index].strip(' \n'))
                while '' in sen_split:
                    sen_split.remove('')
                result = self.__track_reg_find_class(contents, index, sen_split[-1])

            elif contents[index].find('const') >= 0:
                sen_split = re.split('[ ,{}]', contents[index].strip(' \n'))
                while '' in sen_split:
                    sen_split.remove('')
                if '0x0' == sen_split[-1]:
                    result = []
                else:
                    result = []
                    print('---> WARNING: const => should be 0x0: ' + contents[index])

            else:
                print(contents[0])
                print(index)
                print('---> WARNING: asynchrony => backtrack failed: ' + contents[index])
                return []

        return result

    ##
    # function: Find all classes that extend from Thread.
    # @param file_path: The target path
    # 
    def __find_thread(self, file_path):
        # Don't scan the Android package
        if 'android' == file_path:
            return

        if '' == file_path:
            target_path = self.__smali_folder
        else:
            target_path = self.__smali_folder + os.path.sep + file_path

        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                for item in os.listdir(target_path):
                    if '' == file_path:
                        self.__find_thread(item)
                    else:
                        self.__find_thread(file_path + os.path.sep + item)
            else:
                # Get each lines of the smali file
                smali_file = open(target_path, 'r')
                file_contents = []
                try:
                    file_contents = smali_file.readlines()
                finally:
                    smali_file.close()

                if 'Ljava/lang/Thread;' == file_contents[1].strip(' \n').split(' ')[-1]:
                    self.__thread_list.append(file_contents[0].strip(' \n').split(' ')[-1])

    ##
    # function: Other objects get the aFCG from this method.
    # @return: The dictionary storing the aFCG information 
    #
    def get_aFCG(self):
        return self.__afcg

    ##
    # function: Other objects get the raFCG from this method.
    # @return: The dictionary storing the raFCG information 
    #
    def get_raFCG(self):
        return self.__rafcg

