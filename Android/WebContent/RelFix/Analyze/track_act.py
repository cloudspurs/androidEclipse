#!/usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Sep 29th, 2015
# Description: Track methods for finding the activity where the resource should be released.
#

import os

from constant import *

##
# function: Judge whether we need more track.
# @param track_list: The functions we are tracking
# @param act_list: All activities in the app
# @return: True if we need more track, False if not
#
def need_more_track(track_list, act_list):
    result = False

    i = 0
    while i < len(track_list):
        if 0 == track_list[i][1]:
            func_class = track_list[i][0].split(';->')[0].lstrip('L')
            func_name = track_list[i][0].split(';->')[1].split('(')[0]
            
            if not func_name in Constants._callback_list:
                result = True
            else:
                if func_class in act_list:
                    track_list[i][1] = 1
                else:
                    result = True

        if 1 == track_list[i][1] and track_list[i][0].find('->') >= 0:
            track_list[i][0] = track_list[i][0].split('->')[0]
            if track_list[i] in track_list[:i]:
                track_list.remove(track_list[i])
                i -= 1
        i += 1

    return result

##
# function: Find the activity or the service a resource should be released.
# @param res: All leaked resources
# @param rfcg: The rFCG
# @param rafcg: The raFCG
# @param act_list: All activities in the app
#
def track_activity(res, rfcg, rafcg, act_list):
    for each_res in res:
        track_list = []
        track_list.append(['L' + each_res.get_func_path()[:-6] + ';->' + each_res.get_func_name(), 0])
        trash_list = []
        while need_more_track(track_list, act_list):
            i = 0
            while i < len(track_list):
                if 0 == track_list[i][1]:
                    if 0 == len(rfcg[track_list[i][0]]):
                        if track_list[i][0] in rafcg:
                            for item in rafcg[track_list[i][0]]:
                                if not [item, 1] in track_list:
                                    track_list.append([item, 1])
                            trash_list.append(track_list[i][0])
                            del(track_list[i])
                            i -= 1
                        else:
                            track_list[i][1] = 3
                    else:
                        for new_func in rfcg[track_list[i][0]]:
                            if not [new_func, 2] in track_list and not new_func in trash_list:
                                track_list.append([new_func, 2])
                        trash_list.append(track_list[i][0])
                        del(track_list[i])
                        i -= 1
                i += 1

            for each_func in track_list:
                if 2 == each_func[1]:
                    each_func[1] = 0

        each_res.set_trace_func(track_list)








