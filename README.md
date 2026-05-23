# 代码文档生成工具
个人独立开发轻量化工具，用于Git仓库源码拉取与自动化项目文档生成

## 版本迭代
V1.0 基础版：项目增删、代码克隆、本地数据存储
V1.1 优化版：完善异常捕获、日志记录、缓存清理、接口健壮性优化

## 技术栈
- 后端：Python3 + Flask
- 数据库：SQLite 轻量数据库
- 依赖工具：Git源码克隆
- 前端：原生HTML+CSS+JavaScript

## 运行步骤
1. 安装依赖：pip install -r requirements.txt
2. 按需修改.env配置参数
3. 启动服务：python server/app.py
4. 浏览器访问：http://localhost:3000
