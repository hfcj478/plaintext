# -*- coding: utf-8 -*-
# 文档管理接口
from flask import Blueprint, request, jsonify
import sqlite3
import time
import os
from server.utils.log_util import write_log

doc_bp = Blueprint("doc", __name__, url_prefix="/api/doc")

# 获取项目文档列表
@doc_bp.get("/list")
def get_doc_list():
    try:
        pid = request.args.get("pid")
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM doc WHERE pid=?", (pid,))
        data = cur.fetchall()
        conn.close()
        return jsonify({"code": 1, "data": data})
    except Exception as e:
        write_log(f"查询文档异常：{e}")
        return jsonify({"code": 0, "data": []})

# 保存文档内容
@doc_bp.post("/save")
def save_document():
    try:
        info = request.get_json()
        pid = info.get("pid")
        title = info.get("title", "")
        content = info.get("content", "")
        now_time = int(time.time())

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        sql = "INSERT INTO doc(pid, title, content, create_time) VALUES (?,?,?,?)"
        cur.execute(sql, (pid, title, content, now_time))
        conn.commit()
        conn.close()
        write_log(f"项目{pid}文档保存成功")
        return jsonify({"code": 1, "msg": "文档保存完成"})
    except Exception as e:
        write_log(f"文档保存异常：{e}")
        return jsonify({"code": 0, "msg": "保存失败"})

# 读取源码目录
@doc_bp.get("/readFile")
def read_source_file():
    pid = request.args.get("pid")
    source_path = f"temp/{pid}"
    if not os.path.exists(source_path):
        return jsonify({"code": 0, "msg": "源码文件不存在"})
    return jsonify({"code": 1, "path": source_path})
