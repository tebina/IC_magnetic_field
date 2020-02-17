# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 18:53:08 2020

@author: nasredine
"""

def split_plus (line):
    new_line=line.split("+")
    return new_line


def split_space (line):
    new_line=line.split()
    return new_line


def split_semic (line):
    new_line=line.split(":")
    return new_line


def split_parentheses (info):
    #returns the info contained between paretheses as info list 
    new_info = []
    make_list = False
    current_list = []
    for idx in range ( len(info)):
        if info[idx] == "(" : 
            make_list = True
        elif info[idx] == ")" :
            make_list == False
            new_info.append(current_list)
            current_list = []
        else:
            if make_list : 
                current_list.append(info[idx])
            else:
                new_info.append(info[idx])
    return new_info