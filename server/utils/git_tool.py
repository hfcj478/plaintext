# -*- coding: utf-8 -*-
# 仓库克隆工具
import git
import os
import shutil
from server.utils.log_util import write_log

def clone_git_code(git_url, pid):
    """克隆远程Git仓库代码"""
    try:
        folder_path = f"temp/{pid}"
        # 清理旧缓存
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.mkdir(folder_path)
        # 执行克隆
        git.Repo.clone_from(git_url, folder_path)
        write_log(f"项目{pid}源码克隆成功")

        # 更新数据库状态
        import sqlite3
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute("UPDATE project SET status=? WHERE id=?", ("解析完成", pid))
        conn.commit()
        conn.close()
    except Exception as e:
        err_info = f"项目{pid}克隆失败：{str(e)}"
        write_log(err_info)
