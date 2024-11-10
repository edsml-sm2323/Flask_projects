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
migrate = Migrate(app, db)
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

    articles = db.relationship("Article", back_populates="author")
# 之后将这个表映射到数据库中
with app.app_context():
    db.create_all()

@app.route('/user/add')
def add_user():
    user1 = User_ORM(username="msy", password="msyhs233")

    # 向数据库中添加一个信息
    db.session.add(user1)
    db.session.commit()

    return "对象创建成功"

@app.route('/user/query')
def query_user():
    # 有两种查询方式
    # get: 根据primary key进行查找
    # user = User_ORM.query.get(1)
    # print(user.username)
    # filter:
    # 返回的是QuerySet对象
    users = User_ORM.query.filter_by(username="msy")
    for user in users:
        print(user.username)

    return "数据查找成功"

@app.route('/user/update')
def update_user():
    user = User_ORM.query.filter_by(username="msy")[0]
    user.password = "222222"
    db.session.commit()

    return "数据修改成功"

@app.route('/user/delete')
def delete_user():
    user = User_ORM.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "数据删除成功"

# 创建一个Article的ORM模型
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User_ORM", back_populates="articles")

with app.app_context():
    db.create_all()

# 添加两篇文章对应作者
@app.route("/article/add")
def article_add():
    article1 = Article(title="Flask学习大纲", text="Flaskxxxx")
    article1.author = User_ORM.query.get(2)

    article2 = Article(title="Django学习大纲", text="Django最全学习大纲")
    article2.author = User_ORM.query.get(2)

    # 添加到session中
    db.session.add_all([article1, article2])
    # 同步session中的数据到数据库中
    db.session.commit()
    return "文章添加成功！"

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

