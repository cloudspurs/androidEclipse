#!/usr/bin/pyhon
#coding=utf-8

##
# Author: Jierui Liu (liujierui@gmail.com)
# Date: Sep 15th, 2015
# Description: Add class fields for saving arguments.
#

import os

##
# functon: Add static field in a class.
# @param contents: The smali file's contents
# @param field_name: The identity of the field
# @param field_type: The type of the field
#
def add_static_field(contents, field_name, field_type):
    new_contents = []
    new_contents.append('\n')
    new_contents.append('.field public static ' + field_name + ':' + field_type + '\n')
    
    contents += new_contents
    
##
# function: Use different operation according to the target variable type.
# @param tar_var: The target variable
# @param str_seq: A sequence of strings would be added in smali file
# @param op: The operation
# @param op_arg: The arguments of the operation
#
def add_op_sentence(tar_var, str_seq, op, op_arg):
    if tar_var[0].find('L') >= 0:
        str_seq.append('    ' + op + '-object ' + op_arg)
    elif tar_var[0].find('I') >= 0 or tar_var[0].find('F') >= 0:
        str_seq.append('    ' + op + ' ' + op_arg)
    elif tar_var[0].find('Z') >= 0:
        str_seq.append('    ' + op + '-boolean ' + op_arg)
    elif tar_var[0].find('B') >= 0:
        str_seq.append('    ' + op + '-byte ' + op_arg)
    elif tar_var[0].find('C') >= 0:
        str_seq.append('    ' + op + '-char ' + op_arg)
    elif tar_var[0].find('S') >= 0:
        str_seq.append('    ' + op + '-short ' + op_arg)
    elif tar_var[0].find('D') >= 0 or tar_var[0].find('J') >= 0:
        str_seq.append('    ' + op + '-wide ' + op_arg)
    else:
        print('---> ERROR: variable type error')

