# -*- coding: utf-8 -*-
# 服务主启动入口
from flask import Flask
from flask_cors import CORS
import sqlite3
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
app = Flask(__name__)
CORS(app)

# 初始化数据库表结构
def init_database():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    # 项目表
    cur.execute('''
    CREATE TABLE IF NOT EXISTS project(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        git_url TEXT NOT NULL,
        status TEXT,
        create_time INTEGER
    )
    ''')
    # 文档表
    cur.execute('''
    CREATE TABLE IF NOT EXISTS doc(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pid INTEGER,
        title TEXT,
        content TEXT,
        create_time INTEGER
    )
    ''')
    conn.commit()
    conn.close()

init_database()

# 注册路由
from server.api.project import project_bp
from server.api.doc import doc_bp
app.register_blueprint(project_bp)
app.register_blueprint(doc_bp)

# 首页访问
@app.route("/")
def index_page():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    debug_mode = os.getenv("DEBUG") == "True"
    print(f"服务启动成功，访问地址：http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
