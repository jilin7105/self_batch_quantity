#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/5 下午5:25
# @Author  : yyq
# @Site    : 
# @File    : videoOut.py
# @Software: PyCharm
from flask import Blueprint, jsonify, redirect, url_for
from moviepy.editor import *
from flask import request,render_template
from moviepy.editor import VideoFileClip, concatenate_videoclips,ImageClip

from cut import add_white_edge
from dataservice.database import *
from movieAbout import action, CreatedEnding
video_bp = Blueprint('videoOut', __name__)


@video_bp.route("/delete/<int:video_id>", methods=["POST"])
def delete(video_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM videoOut WHERE id=?", (video_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@video_bp.route("/edit/<int:video_id>", methods=["GET", "POST"])
def edit(video_id):
    conn = get_db_connection()
    if request.method == "POST":
        video_path = request.form["video_path"]
        image_path = request.form["image_path"]
        status = request.form["status"]
        path = request.form["path"]
        conn.execute("UPDATE videoOut SET video_path=?, image_path=?, status=?, path=? WHERE id=?",
                     (video_path, image_path, status, path, video_id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    else:
        cursor = conn.execute("SELECT * FROM videoOut WHERE id=?", (video_id,))
        video = cursor.fetchone()
        conn.close()
        return render_template("edit.html", video=video)

@video_bp.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM videoOut WHERE video_path LIKE ? OR image_path LIKE ? OR path LIKE ?",
                          (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    videos = cursor.fetchall()
    conn.close()
    return render_template("index.html", videos=videos)