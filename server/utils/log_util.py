# -*- coding: utf-8 -*-
# 简易日志工具
import os
import time

LOG_DIR = "../logs"
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

def write_log(content):
    """写入运行日志"""
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_file = os.path.join(LOG_DIR, "run.log")
    log_msg = f"[{now}] {content}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_msg)
    print(log_msg.strip())
