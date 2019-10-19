from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from  flask_login import LoginManager

app = Flask(__name__)
# 导入配置文件
app.config.from_object(config)
# 建立数据库关系
db = SQLAlchemy(app)
# 绑定app和数据库
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models