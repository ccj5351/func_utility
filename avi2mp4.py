# !/usr/bin/env python3
# -*-coding:utf-8-*-
# @file: avi2mp4.py
# @brief:
# @author: Changjiang Cai, ccai1@stevens.edu, caicj5351@gmail.com
# @version: 0.0.1
# @creation date: 25-08-2020
# @last modified: Wed 12 May 2021 01:59:18 AM EDT

import sys
import os
def convert_avi_to_mp4(avi_file_path, output_name):
    "ffmpeg -i {input} -c:v libx264 -crf 19 -preset veryslow -c:a libfdk_aac -b:a 192k -ac 2 ou"
    os.popen("ffmpeg -i {input} -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 {output}.mp4".format(
        input = avi_file_path, 
        output = output_name)
        )
    return True

def convert_avi_to_mp4_lossless(avi_file_path, output_name):
    # simply re-mux the streams from AVI container to MP4 container.
    # There is no re-encoding so there is no quality loss. 
    os.popen("ffmpeg -i {input} -c copy -map 0 {output}.mp4".format(
        input = avi_file_path, 
        output = output_name
        )
        )
    return True
#convert_avi_to_mp4('./cbmv-gcnet-imgs1150.avi', 'cbmv-gcnet-imgs1150.mp4')
#convert_avi_to_mp4_lossless('./cbmv-gcnet-imgs1150.avi', 'cbmv-gcnet-imgs1150')
#convert_avi_to_mp4_lossless('./CVPR2020-CBMVPSMNet-raw.avi', 'ms-psmnet')
#convert_avi_to_mp4_lossless('/media/ccjData1_HDD/Dropbox/Towrads_Ph.D._CCJ/3DV-2020-two-papers-Oct_2/msnet/msnet_fps_25_used_in_ppt.avi', 
#        'msnet_fps_25_used_in_ppt')
convert_avi_to_mp4_lossless(
        '/home/ccj/mvs-depth/results/fig-plot/qual-dep.avi', 
        '/home/ccj/mvs-depth/results/fig-plot/qual-dep-convert',
        )
sys.exit()

from converter import Converter
conv = Converter()

#info = conv.probe('./寿糕10.AVI')

convert = conv.convert('./cbmv-gcnet-imgs1150.avi', 'cbmv-gcnet-imgs1150.mp4', {
        'format': 'mp4',
        'audio': {
            'codec': 'aac',
            'samplerate': 11025,
            'channels': 2
            },
         'video': {
             #'codec': 'hevc',
             'codec': 'h264',
             'width': 620,
             'height': 564,
             'fps': 10
        }})

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')
