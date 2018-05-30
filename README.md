## shadowsocker
A management system of shadowsocks

## 项目运行
```
# 使用 pip 安装项目所需的库
pip install -r requirement.txt

# 对数据库进行初始化
python manage.py db init

# 初始化后，还需要进入 Shell 生成数据表
python manage.py shell
>>> db.create_all()
>>> exit()

# 设置服务器的环境和一些参数，避免敏感信息被泄露
# 如果在 Linux 和 Mac OS X 中使用 bash，则按照以下设置：
export FLASK_CONFIG=production

# Windows 用户则按照下面方式设置：
set FLASK_CONFIG=production

# 除了 FLASK_CONFIG 以外，还需要设置以下变量：
MAIL_USERNAME：发送邮件的邮箱的账号
MAIL_PASSWORD：发送邮件的邮箱的密码

```
