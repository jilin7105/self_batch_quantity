import sqlite3
import json

DATABASE_FILE = 'parameters.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 检测表是否存在，如果不存在则创建
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='parameters'")
    result = cursor.fetchone()
    if not result:
        cursor.execute('''
            CREATE TABLE parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parameter TEXT,
                status INTEGER DEFAULT 0,
                result TEXT
            )
        ''')
        conn.commit()

    # 检测表是否存在，如果不存在则创建
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='videoOut'")
    result = cursor.fetchone()
    if not result:
        cursor.execute('''
               CREATE TABLE videoOut (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   job_id INTEGER ,
                   video_path TEXT,
                   image_path TEXT,
                   status INTEGER DEFAULT 0,
                   path TEXT
               )
           ''')
        conn.commit()

    conn.close()


#
def get_videoOut_count_by_imagePAth(path):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) as count FROM videoOut WHERE image_path = ?   LIMIT 1",(path,) )
    result = cursor.fetchone()[0]

    conn.close()

    if result:


        return result
    else:
        return 0


def set_videoOut(job_id,video_path,image_path,path):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 插入参数记录
    cursor.execute("INSERT INTO videoOut (job_id, video_path,image_path,path) VALUES (?, ?,?,?)", (job_id,video_path,image_path,path))
    conn.commit()

    conn.close()


def set_job(data):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 插入参数记录
    cursor.execute("INSERT INTO parameters (parameter, status) VALUES (?, 0)", (json.dumps(data),))
    conn.commit()

    conn.close()


def update_job_status(job_id, new_status):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 更新任务状态
    cursor.execute("UPDATE parameters SET status = ? WHERE id = ?", (new_status, job_id))
    conn.commit()

    conn.close()


def update_job_result(job_id, result):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 更新任务处理结果
    cursor.execute("UPDATE parameters SET result = ? WHERE id = ?", (json.dumps(result), job_id))
    conn.commit()

    conn.close()


def get_pending_job():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 获取状态为0的任务
    cursor.execute("SELECT id, parameter FROM parameters WHERE status = 0 LIMIT 1")
    result = cursor.fetchone()

    conn.close()

    if result:
        job_id, parameter = result

        # 访问字段值
        job = {
            'id': job_id,
            'parameter': parameter
        }
        return job
    else:
        return None

def get_all_redy_jobs():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 获取所有任务
    cursor.execute("SELECT * FROM parameters where status =0")
    results = cursor.fetchall()

    conn.close()

    jobs = []
    for row in results:
        job_id, parameter, status, result = row
        job = {
            'id': job_id,
            'parameter': parameter,
            'status': status,
            'result': result
        }
        jobs.append(job)

    return jobs


def get_all_jobs():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # 获取所有任务
    cursor.execute("SELECT * FROM parameters")
    results = cursor.fetchall()

    conn.close()

    jobs = []
    for row in results:
        job_id, parameter, status, result = row
        job = {
            'id': job_id,
            'parameter': json.loads(parameter),
            'status': status,
            'result': result
        }
        jobs.append(job)

    return jobs