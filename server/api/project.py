# -*- coding: utf-8 -*-
# 项目管理接口
from flask import Blueprint, request, jsonify
import sqlite3
import time
import os
import shutil
from server.utils.log_util import write_log
from server.utils.git_tool import clone_git_code

project_bp = Blueprint("project", __name__, url_prefix="/api/project")

# 查询项目列表
@project_bp.get("/list")
def get_project_list():
    try:
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM project ORDER BY create_time DESC")
        rows = cur.fetchall()
        conn.close()
        res_list = []
        for row in rows:
            res_list.append({
                "id": row[0],
                "name": row[1],
                "git_url": row[2],
                "status": row[3],
                "create_time": row[4]
            })
        return jsonify({"code": 1, "data": res_list})
    except Exception as e:
        write_log(f"查询项目异常：{e}")
        return jsonify({"code": 0, "msg": "数据查询失败"})

# 新增项目
@project_bp.post("/add")
def add_project():
    try:
        data = request.get_json()
        name = data.get("name", "").strip()
        git_url = data.get("url", "").strip()
        if not name or not git_url:
            return jsonify({"code": 0, "msg": "项目名和仓库地址不能为空"})

        create_time = int(time.time())
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        sql = "INSERT INTO project(name, git_url, status, create_time) VALUES (?,?,?,?)"
        cur.execute(sql, (name, git_url, "代码拉取中", create_time))
        conn.commit()
        pid = cur.lastrowid
        conn.close()

        write_log(f"新增项目{pid}：{name}")
        clone_git_code(git_url, pid)
        return jsonify({"code": 1, "msg": "项目添加成功，后台开始拉取源码", "pid": pid})
    except Exception as e:
        write_log(f"新增项目异常：{e}")
        return jsonify({"code": 0, "msg": "项目添加失败"})

# 删除项目
@project_bp.post("/del")
def delete_project():
    try:
        pid = request.get_json().get("id")
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM project WHERE id=?", (pid,))
        cur.execute("DELETE FROM doc WHERE pid=?", (pid,))
        conn.commit()
        conn.close()

        # 清理本地缓存
        cache_path = f"temp/{pid}"
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
        write_log(f"删除项目{pid}及缓存文件")
        return jsonify({"code": 1, "msg": "项目已彻底删除"})
    except Exception as e:
        write_log(f"删除项目异常：{e}")
        return jsonify({"code": 0, "msg": "删除失败"})

# 更新项目状态
@project_bp.post("/updateStatus")
def update_status():
    try:
        data = request.get_json()
        pid = data.get("id")
        status = data.get("status")
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("UPDATE project SET status=? WHERE id=?", (status, pid))
        conn.commit()
        conn.close()
        return jsonify({"code": 1})
    except Exception as e:
        write_log(f"状态更新异常：{e}")
        return jsonify({"code": 0})
