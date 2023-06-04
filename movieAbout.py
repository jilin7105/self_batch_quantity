#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 上午8:22
# @Author  : yyq
# @Site    : 
# @File    : movieAbout.py
# @Software: PyCharm
import json
import datetime


from moviepy.editor import *
from flask import request
from moviepy.editor import VideoFileClip, concatenate_videoclips,ImageClip
from cut import add_white_edge


def action(data_json):
    time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data = data_json
    data = json.loads(data)
    name = "static/video/素材/" + data["name"]
    fengmian = "static/video/图片/" + data["fengmian"]
    new_fengmain = "static/video/切图/" + data["fengmian"]
    cutlist = data["cutlist"]

    clip1 = VideoFileClip(name)
    clip1 = clip1.resize((720, 1280))
    size = (720, 1280)

    add_white_edge(fengmian, new_fengmain, size[0], size[1])
    im = ImageClip(new_fengmain, duration=0.1)

    videoout_list = []
    for item in cutlist:

        start = item['start']
        end = item['end']
        clipVideo = clip1.subclip(start, end)
        threads = 8
        bgclip = clipVideo
        c = ColorClip(size, color=(255, 255, 255), duration=clipVideo.duration)
        newc = c.fx(vfx.mask_color, color=(100, 100, 100), thr=140, s=2)
        bgclip = CompositeVideoClip([bgclip, newc])

        newclip = CompositeVideoClip(
            [bgclip, clipVideo.resize(0.87).set_position("center")], size, (255, 255, 255), True)
        final_clip = concatenate_videoclips([im, newclip])

        final_clip.write_videofile("static/video/导出/({}){}({}-{}).mp4".format(data["name"], time_name, start, end)
                                   , threads=threads
                                   , codec="libx264",
                                   audio_codec="aac")
        final_clip.close()
        videoout_list.append("static/video/导出/({}){}({}-{}).mp4".format(data["name"], time_name, start, end))
    return {
        "data": videoout_list
    }


def setText(video,Text):
    TextClip.default_font = 'front/Sonti.ttc'
    text = TextClip("Hello, World!", fontsize=40, color='yellow', font='custom_font',
                    stroke_color='black', stroke_width=2, align='center')
    text = text.set_position(('center', 'center')).set_duration(0.1).set_start(0)
    final_clip = CompositeVideoClip([video, text])
    return final_clip


def CreatedEnding(file_name):
    time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


    original_video = VideoFileClip("static/video/导出/"+file_name)
    dubbing_video = VideoFileClip("static/video/音频/ending.mp4")




    # 获取配音文件音频长度
    dubbing_audio_duration = dubbing_video.duration
    original_video_duration = original_video.duration
    # 获取原视频指定时间段的音频
    start_time = 0
    end_time = original_video_duration - dubbing_audio_duration

    original_video1 = original_video.subclip(start_time, end_time)
    original_video2 = original_video.subclip(end_time)
    original_video3 = original_video2.set_audio(dubbing_video.audio)
    # 拼接音频

    final_video = concatenate_videoclips([original_video1, original_video3])


    # original_video1.write_videofile("static/video/导出/ending/({})1-ending.mp4".format(time_name), codec="libx264")
    # original_video3.write_videofile("static/video/导出/ending/({})2-ending.mp4".format(time_name), codec="libx264")


    # audio_video_time = audio_video.duration
    # # 提取音频
    # extracted_audio = audio_video.audio
    # original_video_time = original_video.duration
    # # 关闭原视频在指定时间段的声音
    # start_time = original_video_time - audio_video_time  # 开始关闭声音的时间（秒）
    # end_time = original_video_time  # 结束关闭声音的时间（秒）
    # original_video = original_video.audio_fadeout(end_time - start_time, start_time)
    #




    # # 将提取的音频添加到原视频的结尾
    # final_video = concatenate_videoclips([original_video, extracted_audio])

    # 输出最终视频
    final_video.write_videofile("static/video/导出/ending/({})-ending.mp4".format(time_name), audio_codec="aac")