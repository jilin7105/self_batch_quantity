import datetime
import json
import time
import base64

from flask import Flask, render_template, jsonify
from moviepy.editor import *
from flask import request
from moviepy.editor import VideoFileClip, concatenate_videoclips,ImageClip

from cut import add_white_edge
from dataservice.database import *
from movieAbout import action, CreatedEnding
from routes.index import index_bp
from routes.videoOut import video_bp


app = Flask(__name__)
init()
app.register_blueprint(index_bp)
app.register_blueprint(video_bp, url_prefix='/video')
# @app.route('/')
# def home():
#     return render_template("home.html")
#
# @app.route('/action')
# def index():
#     info = os.listdir("static/video/素材")
#     base_path = os.getcwd()
#     images = os.listdir("static/video/图片")
#     sucai_dir = os.path.join(base_path, "video/素材")
#     # return "ok"
#     return render_template("test.html", context={
#         "path": "/static/video/素材/",
#         "list": info,
#         "image": {
#             "path": "/static/video/图片/",
#             "images": images
#         }
#     })
#
# @app.route('/cutvide', methods=['POST'])
# def info():
#     # time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     data = request.get_data()
#     data = json.loads(data)
#     # name = "static/video/素材/"+data["name"]
#     # fengmian = "static/video/图片/"+data["fengmian"]
#     # new_fengmain =  "static/video/切图/"+data["fengmian"]
#     # cutlist =  data["cutlist"]
#     #
#     # clip1 = VideoFileClip(name)
#     # clip1 = clip1.resize((720,1280))
#     # size = (720,1280)
#     #
#     # add_white_edge(fengmian,new_fengmain,size[0],size[1] )
#     # im = ImageClip(new_fengmain,duration=0.1)
#     #
#     #
#     # videoout_list = []
#     # for item in cutlist :
#     #     print(item)
#     #     start = item['start']
#     #     end = item['end']
#     #     clipVideo = clip1.subclip(start, end)
#     #     threads = 8
#     #     bgclip = clipVideo
#     #     c = ColorClip(size, color=(255, 255, 255), duration=clipVideo.duration)
#     #     newc = c.fx(vfx.mask_color, color=(100, 100, 100), thr=140, s=2)
#     #     bgclip = CompositeVideoClip([bgclip, newc])
#     #
#     #     newclip = CompositeVideoClip(
#     #         [bgclip, clipVideo.resize(0.87).set_position("center")], size, (255, 255, 255), True)
#     #     final_clip = concatenate_videoclips([im, newclip])
#     #
#     #     final_clip.write_videofile("static/video/导出/({}){}({}-{}).mp4".format(data["name"],time_name,start,end)
#     #                                 ,threads=threads
#     #                                 ,codec="libx264")
#     #     final_clip.close()
#     #     videoout_list.append("static/video/导出/({}){}({}-{}).mp4".format(data["name"],time_name,start,end))
#     set_job(data)
#
#     return {
#         "ok":data
#     }
#
# @app.route('/job_action', methods=['GET'])
# def get_parameter():
#     # 获取状态为0的待处理任务
#     job = get_pending_job()
#
#     if job is not  None:
#         return {}
#     try:
#
#         update_job_status(job['id'], 1)
#         # 在这里执行你的处理逻辑，例如调用处理函数，处理参数
#         res = action(job['parameter'] , job['id'])
#         print(res)
#         # 如果成功处理，更新任务状态为2
#         update_job_status(job['id'], 2)
#         update_job_result(job['id'], res)
#
#
#     except Exception as e:
#
#         # 如果处理出错或失败，更新任务状态为0
#         update_job_status(job['id'], 0)
#         print(e)
#         # 在这里可以记录错误日志或执行其他操作
#
#     return "ok"
#
#
# @app.route('/job_action_all', methods=['GET'])
# def get_parameter_all():
#     # 获取状态为0的待处理任务
#     jobs = get_all_redy_jobs()
#
#     for job in jobs:
#         try:
#
#             update_job_status(job['id'], 1)
#             # 在这里执行你的处理逻辑，例如调用处理函数，处理参数
#             res = action(job['parameter'], job['id'])
#             print(res)
#             # 如果成功处理，更新任务状态为2
#             update_job_status(job['id'], 2)
#             update_job_result(job['id'], res)
#
#
#         except Exception as e:
#
#             # 如果处理出错或失败，更新任务状态为0
#             update_job_status(job['id'], 0)
#             print(e)
#             # 在这里可以记录错误日志或执行其他操作
#
#     return "ok"
#
#
# @app.route('/ending')
# def ending():
#     # 读取指定文件夹下的所有 MP4 文件
#     import os
#     folder = 'static/video/导出'
#     files = [f for f in os.listdir(folder) if f.endswith('.mp4')]
#
#     # 渲染模板，并传递文件列表到页面
#     return render_template('ending.html', files=files)
#
#
# @app.route('/create_ending')
# def create_ending():
#     # 获取参数文件名
#     filename = request.args.get('filename')
#
#     # 调用你的处理逻辑，例如调用 MoviePy 进行处理
#     # ...
#     CreatedEnding(filename)
#
#     return '处理完成：{}'.format(filename)
#
#
# @app.route('/tasks')
# def show_tasks():
#     # 获取所有任务
#     tasks = get_all_jobs()
#
#     return render_template('tasks.html', tasks=tasks)
#
#
# @app.route('/update_status', methods=['POST'])
# def update_status():
#     task_id = int(request.form['task_id'])
#     status = int(request.form['status'])
#
#     # 更新任务状态
#     update_job_status(task_id, status)
#
#     return 'Status updated successfully.'
#
# @app.route('/jobs')
# def get_jobs():
#     # 获取所有任务
#     jobs = get_all_jobs()
#
#     return jsonify(jobs)

if __name__ == '__main__':
    app.run(debug=True)
