# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将依赖文件复制到工作目录
COPY requirements.txt .

# 安装依赖
# 建议在构建镜像时使用 --no-cache-dir 以减小镜像大小
# 确保系统依赖项（如 mysql client 开发库）已安装，如果 mysqlclient 需要编译
# 对于 Debian/Ubuntu (python:*-slim 通常基于此):
# RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc && rm -rf /var/lib/apt/lists/*
# 如果 mysqlclient 安装仍然有问题，可以考虑使用 pymysql (需要修改 SQLAlchemy URI)
RUN pip install --no-cache-dir -r requirements.txt

# 将项目文件复制到工作目录
COPY . .

# 声明 Flask 应用的端口 (与 app.run 或 Gunicorn 绑定的一致)
EXPOSE 5000

# 定义环境变量 (可选, 但推荐)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# 对于生产环境，FLASK_ENV 通常设置为 production (或不设置，让 Gunicorn 处理)
# ENV FLASK_ENV=production

# 运行应用的命令
# 对于开发，可以使用: CMD ["flask", "run"]
# 对于生产，推荐使用 Gunicorn:
# Gunicorn 会在 app.py 中寻找名为 'app' 的 Flask 实例
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]