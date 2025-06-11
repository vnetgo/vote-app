# 基于 Excel 的 Flask 投票系统

这是一个使用 Flask 构建的 Web 应用程序，允许用户通过从 Excel 文件导入的选项进行投票。它支持多用户投票，并使用 MySQL 作为数据库后端。

## 功能

- 用户注册和登录
- 从 Excel 文件动态加载投票选项
- 用户投票（通常每人每选项一票）
- 实时投票结果显示（表格和图表）
- 基于 Flask-SQLAlchemy 的 MySQL 数据库集成
- 基于 Flask-Login 的会话管理

## 项目结构

```
/vote
|-- app.py                   # Flask 主应用程序文件
|-- requirements.txt         # Python 依赖项
|-- votes.html               # 原始的静态 HTML 文件 (参考)
|-- /templates               # Jinja2 HTML 模板
|   |-- base.html            # 基础布局模板
|   |-- login.html           # 用户登录页面
|   |-- register.html        # 用户注册页面
|   |-- votes_dynamic.html   # 动态投票页面
|   |-- results.html         # 投票结果页面
|-- /static
|   |-- /css
|       |-- style.css        # 全局 CSS 样式
|-- README.md                # 本文件
```

## 设置和运行

### 1. 先决条件

- Python 3.7+
- MySQL 服务器
- Git (可选, 用于克隆)

### 2. 克隆仓库 (可选)

```bash
git clone <repository_url>
cd vote
```

### 3. 创建并激活虚拟环境

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖项

```bash
pip install -r requirements.txt
```

### 5. 配置数据库

   a. **创建 MySQL 数据库**:
      在您的 MySQL 服务器中创建一个名为 `voting_db` (或您选择的任何名称) 的数据库。
      例如，使用 MySQL CLI:
      ```sql
      CREATE DATABASE voting_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
      ```

   b. **更新数据库连接字符串**:
      打开 `app.py` 文件。
      找到以下行：
      ```python
      app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlclient://YOUR_MYSQL_USER:YOUR_MYSQL_PASSWORD@localhost/voting_db'
      ```
      将 `YOUR_MYSQL_USER` 和 `YOUR_MYSQL_PASSWORD` 替换为您的实际 MySQL 用户名和密码。如果您的数据库名称或主机不同，也请相应更新。

### 6. 运行应用程序

```bash
python app.py
```

   应用程序将在 `http://127.0.0.1:5000/` 上运行。
   首次运行时，Flask-SQLAlchemy 会自动创建数据库表。

## 使用方法

1.  **注册/登录**: 访问应用程序并注册一个新帐户或使用现有帐户登录。
2.  **上传投票选项 (管理员)**:
    - 登录后，导航到投票页面 (`/vote`)。
    - （此功能的 UI 可能需要进一步完善或移至专门的管理页面）页面底部会有一个“管理：上传投票选项 (Excel)”部分。
    - 准备一个 Excel 文件 (`.xlsx` 或 `.xls`)。该文件应至少包含一列用于投票选项的名称。如果您的 `votes.html` 或后端逻辑期望其他列（如描述），请确保它们存在。
    - 例如，一个简单的 Excel 文件可能如下所示：
      | OptionName | Description       |
      |------------|-------------------|
      | 选项 A     | 这是选项 A 的描述 |
      | 选项 B     | 这是选项 B 的描述 |
      | 选项 C     |                   |
    - 点击“选择Excel文件”，选择您的文件，然后点击“上传文件”。
    - 上传成功后，选项将加载到数据库中，投票页面将刷新显示这些选项。
3.  **投票**: 在投票页面上，您将看到从 Excel 文件加载的选项。点击您选择的选项旁边的“投此一票”按钮。
4.  **查看结果**: 导航到结果页面 (`/results`) 以查看当前投票的统计数据，通常以表格和图表形式显示。

## 注意事项

- **安全性**: `SECRET_KEY` 在 `app.py` 中是随机生成的。对于生产环境，请确保这是一个强大且保密的密钥。
- **MySQL驱动程序**: `mysqlclient` 是推荐的驱动程序。如果遇到安装问题，请查阅其文档以获取特定于操作系统的说明 (可能需要构建工具或开发库)。
- **Excel 解析**: 当前 `app.py` 中的 `/admin/upload_options` 路由有一个用于处理 Excel 上传的占位符。您需要使用像 `openpyxl` 或 `pandas` 这样的库来实现完整的解析逻辑，以从上传的 Excel 文件中读取数据并填充 `VoteOption` 表。原始 `votes.html` 中的 JavaScript 解析逻辑可以作为后端实现的参考。
- **错误处理和验证**: 为了使应用程序更健壮，应添加更全面的错误处理和输入验证。
- **管理员功能**: 当前的 Excel 上传功能对所有登录用户开放。在实际应用中，您需要实现角色管理，以便只有管理员才能上传选项。

## 如何贡献

欢迎提出问题、错误报告和拉取请求。

## 使用 Docker 和 1Panel 进行部署

以下步骤说明了如何使用 Docker 将此 Flask 应用容器化，并通过 1Panel 面板进行部署。

### 1. 先决条件 (除了之前的)

- Docker 已安装在您的部署服务器上 (1Panel 通常会处理 Docker 的安装和管理)。
- 1Panel 已安装并正在运行。
- Docker 镜像仓库 (例如 Docker Hub, Aliyun ACR, Harbor, 或者您可以使用 1Panel 的本地镜像导入功能)。

### 2. 构建 Docker 镜像

在项目根目录 (包含 `Dockerfile` 的地方) 打开终端，运行以下命令来构建 Docker 镜像：

```bash
docker build -t your-username/flask-vote-app:latest .
```

- 将 `your-username/flask-vote-app` 替换为您希望的镜像名称和标签 (例如，您的 Docker Hub 用户名和应用名称)。

**注意关于 `mysqlclient` 的依赖：**
`Dockerfile` 中有一行被注释掉的命令用于安装 `mysqlclient` 的系统依赖：
```dockerfile
# RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc && rm -rf /var/lib/apt/lists/*
```
如果 `pip install mysqlclient` 在构建过程中失败，提示缺少 `mysql_config` 或其他编译错误，您需要取消注释这一行。这将确保构建环境中包含编译 `mysqlclient` 所需的库和工具。

### 3. 推送镜像到仓库 (可选, 但推荐)

如果您的 1Panel 服务器无法直接访问本地构建的镜像，您需要将其推送到一个 Docker 镜像仓库：

```bash
# 首先登录到您的 Docker 仓库 (例如 Docker Hub)
# docker login

docker push your-username/flask-vote-app:latest
```

### 4. 在 1Panel 中部署

1.  **创建 MySQL 数据库服务 (如果尚未创建)**:
    *   登录到您的 1Panel。
    *   导航到 “数据库” -> “MySQL”，创建一个新的 MySQL 数据库实例 (例如 `voting_db`) 和一个专用的用户及密码。
    *   记下数据库的主机名 (通常是服务名，如 `mysql`)、端口 (通常是 `3306`)、数据库名、用户名和密码。1Panel 中的容器通常可以通过服务名相互访问。

2.  **部署 Flask 应用容器**:
    *   导航到 “应用商店” 或 “容器” -> “创建容器/应用”。
    *   选择 “自定义镜像” 或 “Compose” (如果使用 `docker-compose.yml`，但这里我们主要关注直接部署镜像)。
    *   **镜像名称**: 输入您之前构建并推送的镜像名称，例如 `your-username/flask-vote-app:latest`。如果镜像在私有仓库，您可能需要配置 1Panel 的镜像仓库凭据。
    *   **容器名称**: 给您的应用容器起一个名字，例如 `vote-app`。
    *   **端口映射**:
        *   容器端口: `5000` (这是 Gunicorn 在 Dockerfile 中绑定的端口)。
        *   主机端口: 选择一个您服务器上未被占用的端口，例如 `8080`。这样您就可以通过 `http://YOUR_SERVER_IP:8080` 访问应用。
    *   **环境变量**: 这是配置数据库连接的关键。
        *   `SQLALCHEMY_DATABASE_URI`: `mysql+mysqlclient://DB_USER:DB_PASSWORD@DB_HOST:DB_PORT/DB_NAME`
            *   将 `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` 替换为您在 1Panel 中创建的 MySQL 服务的实际凭据和地址。
            *   例如: `mysql+mysqlclient://vote_user:vote_password@mysql:3306/voting_db` (假设 `mysql` 是 1Panel 中 MySQL 服务的名称)。
        *   `SECRET_KEY`: 设置一个强随机字符串作为 Flask 的 `SECRET_KEY`。例如: `openssl rand -hex 32` 生成一个。
        *   `FLASK_APP`: `app.py` (通常已在 Dockerfile 中设置)
        *   `FLASK_RUN_HOST`: `0.0.0.0` (通常已在 Dockerfile 中设置)
    *   **卷挂载 (可选)**:
        *   如果您的应用有需要持久化存储的文件 (例如用户上传的文件，而不是数据库中的数据)，您可以在这里配置卷挂载。对于此投票应用，主要数据在 MySQL 中，所以可能不需要额外的卷挂载，除非您扩展了文件上传功能。
    *   **网络**: 确保应用容器与 MySQL 服务在同一个 Docker 网络中，以便它们可以通过服务名相互通信。1Panel 通常会处理好这一点。
    *   **重启策略**: 设置为 `Always` 或 `Unless Stopped`，以确保容器在意外退出或服务器重启后能自动重启。

3.  **启动应用**:
    *   完成配置后，点击 “创建” 或 “部署”。1Panel 将拉取镜像并启动容器。
    *   查看容器日志以确保应用正常启动，没有数据库连接错误或其他问题。

4.  **访问应用**:
    *   通过您在端口映射中设置的主机端口访问您的应用，例如 `http://YOUR_SERVER_IP:HOST_PORT`。

### 5. 更新应用

当您更新了代码后：

1.  重新构建 Docker 镜像 (使用新的标签，例如 `:v1.1` 或 `:latest`)。
2.  将新镜像推送到您的镜像仓库。
3.  在 1Panel 中，找到您的应用容器，通常会有 “重新部署” 或 “更新镜像” 的选项，您可以指定新的镜像标签来更新正在运行的应用。

### 注意事项 (1Panel 特定)

- **防火墙**: 确保您的服务器防火墙 (以及 1Panel 可能管理的防火墙) 允许访问您为主机端口选择的端口。
- **反向代理**: 为了使用域名和 HTTPS 访问您的应用，您可以在 1Panel 中设置一个反向代理 (例如使用 Nginx 或 OpenResty 应用)，将域名请求代理到您的 Flask 应用容器的主机端口。
- **日志**: 定期检查 1Panel 中容器的日志，以便监控应用状态和排查问题。
- **资源限制**: 根据需要，在 1Panel 中为您的应用容器配置 CPU 和内存限制。