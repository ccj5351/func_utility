# !/usr/bin/env python3
# -*-coding:utf-8-*-
# @file: video_downloader.py
# @brief:
# @author: Changjiang Cai, ccai1@stevens.edu, caicj5351@gmail.com
# @version: 0.0.1
# @creation date: 05-11-2018
# @last modified: Mon Nov  5 13:40:21 2018

from pytube import YouTube
import os
import argparse

def downloadYouTube(videourl, path):
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--videourl', dest = 'url', help = 'YouTube video url', required = True)
    parser.add_argument('--savedir', dest = 'savedir', help = 'YouTube video save directory', default = "~/Downloads/")
    args = parser.parse_args()
    downloadYouTube(args.url, args.savedir)

