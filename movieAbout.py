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
from dataservice.database import get_videoOut_count_by_imagePAth,set_videoOut


def action(data_json,job_id):
    time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data = data_json
    data = json.loads(data)
    name = "static/video/素材/" + data["name"]
    fengmian = "static/video/图片/" + data["fengmian"]
    new_fengmain = "static/video/切图/" + data["fengmian"]
    cutlist = data["cutlist"]

    clip1 = VideoFileClip(name)
    clip1 = clip1.resize((1080, 1920))
    size = (1080, 1920)

    add_white_edge(fengmian, new_fengmain, size[0], size[1])
    im = ImageClip(new_fengmain, duration=0.1)

    videoout_list = []
    for item in cutlist:
        count_info = get_videoOut_count_by_imagePAth(fengmian)
        start = item['start']
        end = item['end']
        clipVideo = clip1.subclip(start, end)
        threads = 8
        bgclip = clipVideo
        c = ColorClip(size, color=(255, 255, 0), duration=clipVideo.duration)
        newc = c.fx(vfx.mask_color, color=(100, 100, 0), thr=140, s=2)
        bgclip = CompositeVideoClip([bgclip, newc])

        newclip = CompositeVideoClip(
            [bgclip, clipVideo.resize(0.85).set_position("center")], size, (255, 255, 255), True)



        final_clip = setText(concatenate_videoclips([im, newclip]),"《第{}集》".format(count_info+1))

        dubbing_video = VideoFileClip("static/video/音频/everyending.mp4")

        # 获取配音文件音频长度
        dubbing_audio_duration = dubbing_video.duration
        original_video_duration = final_clip.duration
        # 获取原视频指定时间段的音频
        start_time = 0
        end_time = original_video_duration - dubbing_audio_duration

        original_video1 = final_clip.subclip(start_time, end_time)
        original_video2 = final_clip.subclip(end_time)
        original_video3 = original_video2.set_audio(dubbing_video.audio)
        # 拼接音频

        final_video = concatenate_videoclips([original_video1, original_video3])

        path_for_cut = "static/video/导出/({}){}({}-{}).mp4".format(data["name"], time_name, start, end)
        final_video.write_videofile(path_for_cut
                                   , threads=threads
                                   , codec="libx264",
                                   audio_codec="aac")
        final_clip.close()
        videoout_list.append(path_for_cut)
        set_videoOut(job_id,name,fengmian,path_for_cut)

    return {
        "data": videoout_list
    }


def setText(video,Text_info):
    TextClip.default_font = 'front/Sonti.ttc'
    text = TextClip(Text_info, fontsize=80, color='yellow', font='custom_font',
                    stroke_color='black', stroke_width=6, align='center')
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

    # 输出最终视频
    final_video.write_videofile("static/video/导出/ending/({})-ending.mp4".format(time_name), audio_codec="aac")







def create_scroll_video(article, video_path, output_path):
    # 文章样式设置
    font_size = 60
    line_spacing = 5
    font_color = 'white'
    background_color = 'black'
    duration_per_word = 1  # 单词持续时间（秒）

    # 计算视频宽度和高度
    video_width = 1080
    video_height = 1920

    # 加载顶部视频
    top_video = VideoFileClip(video_path)
    cropped_video = top_video.crop(x1=0, y1=0, x2=video_height//4, y2= video_width)
    # 创建字幕文本剪辑
    subtitle = TextClip(article, fontsize=font_size, color=font_color, font='Arial', align='center',
                        bg_color=background_color, method='caption', size=(video_width, None)).set_duration(
        duration_per_word * len(article))

    # 设置行间距
    subtitle = subtitle.set_position(('center', video_height//4)).set_position(("center", "bottom"))
    # 保存输出视频
    subtitle.write_videofile(output_path, codec='libx264', audio_codec='aac',fps=24)
    return
    # 创建背景剪辑
    background = ColorClip(size=(video_width, video_height-video_height//4), col=background_color).set_duration(subtitle.duration)

    # 将背景和字幕合并为一个视频
    video = CompositeVideoClip([cropped_video, background.set_position((0, video_height//4)), subtitle])

    # 调整视频大小和比例
    video = video.resize(height=video_height)




