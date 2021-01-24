# !/usr/bin/env python3
# -*-coding:utf-8-*-
# @file: downsample_imgs.py
# @brief:
# @author: Changjiang Cai, ccai1@stevens.edu, caicj5351@gmail.com
# @version: 0.0.1
# @creation date: 13-10-2020
# @last modified: Sat 23 Jan 2021 07:42:04 PM EST

import numpy as np
from PIL import Image

w_min = 200
h_min = 90

def down_sample_png(
        img, # a pillow image;
        scale = 2.0,
        ):
    w, h = img.size
    if w > w_min and h > h_min:
        w_new = int(1.0*w/scale)
        h_new = int(1.0*h/scale)
        res = img.resize((w_new, h_new), Image.BILINEAR)
    else:
        res = None
    return res
        
import os
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    """ for MSNet 3DV 2020 paper """
    if 0:
        mypath = '/media/ccjData3_HDD/Downloads2/qualitatives' 
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        dstpath  = '/media/ccjData3_HDD/Downloads2/qualitatives_small'
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
            print("makedirs '%s' created" % dstpath)

        i = 0
        for f in onlyfiles:
            src_img_name = join(mypath, f)
            img = Image.open(src_img_name)
            res = down_sample_png(img, scale = 1.5)
            if res:
                i += 1
                save_img_name = join(dstpath, f)
                res.save(save_img_name)
        print ("i = ", i)   
    
    """ for DAFNet 3DV 2020 paper """
    if 0:
        mypath = '/media/ccjData3_HDD/Downloads2/img' 
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        dstpath  = '/media/ccjData3_HDD/Downloads2/img_small'
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
            print("makedirs '%s' created" % dstpath)

        i = 0
        for f in onlyfiles:
            if "paper-fig" in f or "spider-vkt2" in f:
                pass
            else:
                src_img_name = join(mypath, f)
                img = Image.open(src_img_name)
                res = down_sample_png(img, scale = 2.0)
                if res:
                    i += 1
                    save_img_name = join(dstpath, f)
                    res.save(save_img_name)
        print ("i = ", i)
    
    """ for PhD thesis proposal """
    if 1:
        #mypath = '/media/ccjData3_HDD/Downloads2/proposal_phd_ccj_2021-Jan23/imgs'
        #mypath = '/media/ccjData3_HDD/Downloads2/proposal_phd_ccj_2021-Jan23/msnet/img'
        mypath = '/media/ccjData3_HDD/Downloads2/proposal_phd_ccj_2021-Jan23/msnet/qualitatives'
        #mypath = '/media/ccjData3_HDD/Downloads2/proposal_phd_ccj_2021-Jan23/dafnet/img'
        dstpath  = mypath + "-low-res-tmp"
        
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)
            print("makedirs '%s' created" % dstpath)

        i = 0
        for f in onlyfiles:
            if ".pdf" in f:
                pass
            """
            elif any([
                "101_" in f,
                "111_" in f,
                "195_" in f,
                "381_" in f,
                "991_" in f,
                "1057_" in f,
                "1062_" in f,
                "1063_" in f,
                "1118_" in f,
                ]
                ):
                if "_L." in f or"_R." in f:
                    scale = 1.0
                else:
                    scale = 1.5
                src_img_name = join(mypath, f)
                img = Image.open(src_img_name)
                res = down_sample_png(img, scale = scale)
                if res:
                    i += 1
                    save_img_name = join(dstpath, f)
                    res.save(save_img_name)
            """
            else:
                src_img_name = join(mypath, f)
                img = Image.open(src_img_name)
                res = down_sample_png(img, scale = 2.0)
                if res:
                    i += 1
                    save_img_name = join(dstpath, f)
                    res.save(save_img_name)
        print ("i = ", i)
