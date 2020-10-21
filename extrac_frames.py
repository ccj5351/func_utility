# !/usr/bin/env python3
# -*-coding:utf-8-*-
# @file: extrac_frames.py
# @brief:
# @author: Changjiang Cai, ccai1@stevens.edu, caicj5351@gmail.com
# @version: 0.0.1
# @creation date: 20-10-2020
# @last modified: Tue 20 Oct 2020 04:04:37 PM EDT

import sys
import argparse

import cv2
import numpy as np
#print(cv2.__version__)

def extractImages(pathIn, pathOut, rate = 1000):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    success = True
    while success:
        # if anyone does not want to extract every frame but wants to 
        # extract frame every one second. So a 1-minute video will give 60 frames(images).
        #vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*rate))    # added this line 
        success, image = vidcap.read()
        print ('Read a new frame: ', success)
        cv2.imwrite( pathOut + "/" + "frame%d.png" % count, image)     # save frame as JPEG file
        count = count + 1

import os
from os import listdir
from os.path import isfile, join
import imageio
from pygifsicle import optimize

def save2_gif(mypath, dstpath):
    #mypath = '/media/ccjData3_HDD/Downloads2/img' 
    gif_path = join(dstpath, 'movie.gif')
    #if os.path.exists(gif_path):
    #    optimize(gif_path, "optimized.gif") # For creating a new one
    #    #optimize(gif_path) # For overwriting the original one
    #else:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyfiles.sort()
    #dstpath  = '/media/ccjData3_HDD/Downloads2/img_small'
    if not os.path.exists(dstpath):
        os.makedirs(dstpath)
        print("makedirs '%s' created" % dstpath)
    with imageio.get_writer(gif_path, mode='I', loop = 0, 
            duration = 0.02 # Note that in the GIF format the duration/delay is expressed 
                       # in hundredths of a second, which limits the precision of the duration.
            ) as writer:
        #for i, f in enumerate (onlyfiles[0:50]):
        for i, f in enumerate (onlyfiles):
            print (" %d / %d : %s " %(i, len(onlyfiles), f))
            src_img_name = join(mypath, f)
            image = imageio.imread(src_img_name)
            writer.append_data(image)
    #optimize(gif_path, "optimized.gif", options = "-03") # For creating a new one

import os
from PIL import Image
def img2mp4(img_dir, fps=15):
    image_files = [join(img_dir, img) for img in os.listdir(img_dir) if img.endswith(".png")]
    image_files.sort()
    import moviepy.video.io.ImageSequenceClip
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(join(img_dir, 'msnet_fps_%d.mp4' % fps), codec="h264")
    #clip.write_videofile(join(img_dir, 'msnet_fps_%d.avi' % fps))

def img2mp4_ffmpeg(fps):
    import ffmpeg
    (
        ffmpeg
        .input('./msnet_combine/frame_*.png', pattern_type='glob', framerate=fps)
        .output('./msnet_combine/movie.avi')
        .run()
    )
    
def img2avi(img_dir, fps):
    image_files = [join(img_dir, img) for img in os.listdir(img_dir) if img.endswith(".png")]
    image_files.sort()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    w = 1245
    h = 564
    out = cv2.VideoWriter(join(img_dir, 'msnet_fps_%d.avi' % fps), fourcc, fps, 
            (w, h) # frameSize
            ) 
    for i, f in enumerate (image_files):
        print (" %d / %d : %s " %(i, len(image_files), f))
        img = cv2.imread(f)
        out.write(img)
    out.release()

def get_msnet_all():
    # get lengend 
    img = Image.open("./legend.png")
    w, h = img.size
    h_new = 188
    w_new = 620
    logo = img.resize((w_new, h_new), Image.BILINEAR)
    msgc_folder = "./frames-ms-gcnet"
    mspsm_folder = "./frames-ms-psmnet"
    msgc_image_files = [ join(msgc_folder, img) for img in os.listdir(msgc_folder) if img.endswith(".png")]
    mspsm_image_files = [ join(mspsm_folder, img) for img in os.listdir(mspsm_folder) if img.endswith(".png")]
    print (len(msgc_image_files))
    msgc_image_files.sort()
    mspsm_image_files.sort()
    
    gap = np.ones((3*h_new, 5, 3)) * 255
    #msgc_image_files = msgc_image_files[0:10]
    #mspsm_image_files = mspsm_image_files[0:10]
    print (len(msgc_image_files))
    #for i, (f1, f2) in enumerate(zip(msgc_image_files, mspsm_image_files)):
    for i in range(len(msgc_image_files)):
        f1 = msgc_image_files[i]
        f2 = mspsm_image_files[i]
        print (i, " / ", len(msgc_image_files), f1, f2)
        img1 = cv2.imread(f1)
        img2 = cv2.imread(f2)
        # replace the upper part in img2 with legend log image;
        img2[:h_new, 0:w_new, :] = np.array(logo)[:,:,:3] # remove alpha channel
        # combine 
        tmp_all = np.concatenate((img1, gap, img2), axis = 1)
        cv2.imwrite("./msnet_combine/frame_%03d.png" %i, tmp_all)


if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--pathIn", help="path to video")
    a.add_argument("--pathOut", help="path to images")
    args = a.parse_args()
    print(args)
    #extractImages(args.pathIn, args.pathOut, rate = 50)
    #save2_gif(args.pathIn, args.pathOut)
    #get_msnet_all()
    #img2mp4(img_dir = "./msnet_combine", fps=25)
    #img2mp4_ffmpeg(fps= 25)
    img2avi(img_dir = "./msnet_combine", fps = 25)
