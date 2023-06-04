#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 上午12:41
# @Author  : yyq
# @Site    : 
# @File    : cut.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
'''
将一张图片修改到指定尺寸并切割为500*500等份的小图片最后再将所有小图拼接为一张完整的原图
Author:bobibo
'''
from PIL import Image
Image.MAX_IMAGE_PIXELS = 2300000000
import sys
import os

#修改尺寸
def add_white_edge(inImgPath, outImgPath, width, height):

    print(f'{inImgPath}')
    inImg: Image.Image = Image.open(inImgPath)
    bgWidth = inImg.width
    bgHeight = inImg.height

    # 创建一个白色背景图片
    bgImg: Image.Image = Image.new("RGB", (bgWidth, bgHeight), (255, 255, 255))
    bgImg.paste(inImg, (0, round((bgHeight - inImg.height) / 2)))

    bgImg.resize((width, height), Image.LANCZOS).save(outImgPath)




