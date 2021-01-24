# !/usr/bin/env python3
# -*-coding:utf-8-*-
# @file: check_latex_label_ref.py
# @brief:
# @author: Changjiang Cai, ccai1@stevens.edu, caicj5351@gmail.com
# @version: 0.0.1
# @creation date: 23-01-2021
# @last modified: Sat 23 Jan 2021 09:42:21 PM EST


import numpy as np
#from PIL import Image
        
import glob
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import re # In Python, we can implement wildcards using the regex (regular expressions) library.
from collections import defaultdict



def find_substring_in_files(file_list, substr_target = "\label", verbose = False):
    labels_dict = defaultdict(int)
    lab_idx = 0
    for f in file_list:
        with open(f, "r") as myfile:
            # Types of wildcards: the asterisk (*)
            # The ".+" symbol is used in place of "*" symbol
            #if re.search("\label{.+}", fread.read():
            i = 0
            for line in myfile:
                i += 1
                line = line.rstrip("\n")
                idx = line.find(substr_target)
                if idx != -1:
                    #find "{"
                    beg_idx = idx
                    while (True):
                        beg_idx+=1
                        if line[beg_idx] == '{' or beg_idx >= len(line)-1:
                            break
                    
                    end_idx = beg_idx
                    while (True):
                        end_idx+=1
                        if line[end_idx] == '}' or end_idx >= len(line)-1:
                            break
                    my_key = line[beg_idx + 1 : end_idx]
                    if labels_dict[my_key] == 0:
                        lab_idx += 1
                    labels_dict[my_key] += 1
                    if verbose and labels_dict[my_key] >= 1:
                        print ("idx %d, key = %s, in file %s, line %d" %(lab_idx, my_key, f, i))
    return labels_dict


if __name__ == "__main__":
    """ for PhD thesis proposal """ 
    if 1:
        mypath = '/media/ccjData3_HDD/Downloads2/proposal_phd_ccj_2021-Jan23'
        #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        #result = [y for x in os.walk(mypath) for y in glob(os.path.join(x[0], '*.tex'), recursive=True)]
        result = list(Path(mypath).rglob("*.[tT][eE][xX]"))
        #for i,f in enumerate(result):
        #    print ("i = ", f) 
        """ 
        If your file is not too large, you can read it into a string, 
        and just use that (easier and often faster than reading and checking line per line)
        """
        
        #find all the labels
        lab_str = "\label"
        labels_dict = find_substring_in_files(result, lab_str, verbose = True)
        print ("find %d labels" %len(labels_dict.keys()))

        #find all the refs
        ref_str = "\\ref"
        print ("find ref")
        ref_dict = find_substring_in_files(result, ref_str, verbose = True)
        print ("find %d refs" %len(ref_dict.keys()))
        
        j = 0
        for lab in labels_dict.keys():
            #print ("checking label %s" %lab)
            if lab not in ref_dict.keys():
                j += 1
                print ("j = %d, label %s NOT used by \\ref{}" %(j, lab))
