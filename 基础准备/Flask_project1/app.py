# 导入Flask类
from flask import Flask, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text

# 使用Flask类创建一个app对象
app = Flask(__name__)

# 写代码规定db的config
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD ="msyhs233"
DATABASE = "flask_project"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'

db = SQLAlchemy(app)

# # 测试数据库是否连接：
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("SELECT 1"))
#         print(rs.fetchone())  # (1,)

# 测试创建一个ORM模型
class User_ORM(db.Model):
    # 表名和类名有什么区别
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
# 之后将这个表映射到数据库中
with app.app_context():
    db.create_all()

# 创建一个User对象
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

# 如何自己创建过滤器
def datetime_format(value, format="%Y-%d-%m %H:%M"):
    return value.strftime(format)

app.add_template_filter(datetime_format, "dformat")
# 创建一个根路由
@app.route('/')
def hello():
    # 创建一个user对象
    # 访问字典或者对象的一个属性的时候 直接食用.调用
    user = User(username="张三", email = "zhangsan@qq.com")
    return render_template("index.html", user=user)

# 如何去给html文件传参数
@app.route('/blog/<blog_id>')
def blog_detail(blog_id):
    return render_template('blog.html', blog_id = blog_id)

# 过滤器的使用 其实就是filter
@app.route('/filter')
def filter_demo():
    user = User(username="张三", email="zhangsan@qq.com")
    nowtime = datetime.now()
    return render_template("filter.html", user=user, nowtime=nowtime)


if __name__ == '__main__':
    app.run()


# debug模式：修改代码并保存可以实时查看更新 出现bug可以在浏览器上看到出错信息
# host: 现在是127.0.0.1 如果在局域网里 设为0.0.0.0 可以使用其他设备输入电脑的ip地址去查看网站效果
# additional options: --host=0.0.0.0
# port: 默认情况下监听的是5000
# additional options: --host=0.0.0.0 --port=8000

