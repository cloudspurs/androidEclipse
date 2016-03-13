#!usr/bin/python
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Data: Sep 6th, 2015
# Description: A class stores all global constants.
#

import os

##
# Class: Store all constants used in entire analysis.
#
class Constants:
    _manifest_file_name = 'AndroidManifest.xml'

    _resource_table_path = '.' + os.path.sep + 'resource_table'

    _log_file_name = 'log_info'

    _apktool = '.' + os.path.sep + 'Tools' + os.path.sep + 'apktool'

    _signapk_file = '.' + os.path.sep + 'Tools' + os.path.sep + 'signapk.jar'
    _pem_file = '.' + os.path.sep + 'Tools' + os.path.sep + 'platform.x509.pem'
    _pk8_file = '.' + os.path.sep + 'Tools' + os.path.sep + 'platform.pk8'

    _ass_list_name = 'relFix_assistant_list'
    _ass_act_manager_name = 'relFix_act_manager'

    _callback_list = ['onCreate', 'onStart', 'onResume', 'onRestart', 'onOptionsItemSelected', 'onPause', 'onStop', 'onDestroy']
