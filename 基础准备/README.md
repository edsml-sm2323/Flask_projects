# Flask开发网站的基础准备

## 版本控制与文件目录

python == 3.9

flask == 2.0.1

MySQL == 9.0

pymysql

```
Flask_project1/
├── app.py                 # 主应用文件，Flask应用的入口
├── config.py              # 配置文件（如数据库配置、密钥等）
├── requirements.txt       # 依赖文件，用于存放所有的Python包依赖
├── .env                   # 环境变量文件，包含密钥和敏感信息
├── static/                # 静态资源文件夹
│   ├── img/               # 图片资源
│   ├── css/               # 样式文件
│   └── js/                # JavaScript文件
├── templates/             # HTML模板文件夹
│   ├── layout.html        # 主布局模板
│   └── index.html         # 首页模板
├── migrations/            # 数据库迁移文件夹（使用Flask-Migrate）
├── models.py              # 数据库模型定义文件
└── README.md              # 项目说明文件
```

## 项目配置

debug: 修改代码不用重启服务，刷新网页即可

host: 现在是127.0.0.1 如果在局域网里 设为0.0.0.0 可以使用其他设备输入电脑的ip地址去查看网站效果 (additional options: --host=0.0.0.0)

port: 默认情况下监听的是5000 (additional options: --host=0.0.0.0 --port=8000)

## app.py

### 根目录
```
@app.route('/')
def hello():
    # 创建一个user对象
    # 访问字典或者对象的一个属性的时候 直接使用.调用
    user = User(username="张三", email = "zhangsan@qq.com")
    return render_template("index.html", user=user)
```

### 传递参数
```
# app.py文件中
@app.route('/blog/<blog_id>')
def blog_detail(blog_id):
    return render_template('blog.html', blog_id = blog_id)

# blog.html文件中
<body>
<h1>这里是blog id 为 {{ blog_id }}</h1>
</body>
```

## 模板渲染
html文件放在templates文件中，使用的是Jinja2模板

### 过滤器 与 自定义过滤器
内置的可以直接使用的Filter: {{user.username|length}}

可以自己自定义Filter：
```
# function编写
def datetime_format(value, format="%Y-%d-%m %H:%M"):
    return value.strftime(format)
    
def filter_demo():
    user = User(username="张三", email="zhangsan@qq.com")
    nowtime = datetime.now()
    return render_template("filter.html", user=user, nowtime=nowtime)
    
# html文件中
{{nowtime|dformat}}

```


### 模板继承
对于一些前端页面中不会发生变化或者变化比较小的部分 可以使用继承父模板的方式降低后期维护成本

{{% extends "base.html"%}}

### 加载静态文件
有三种静态文件

图片, css文件, Javascript文件

```
<img> </img>
<link> </link>
<script> </script>
```


## 数据库连接
pymysql: 链接数据库
ORM模型：对象关系映射 不用SQL语句 一个ORM模型与数据库中的一张表对应

### 建立与数据库的链接
```
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD ="msyhs233"
DATABASE = "flask_project"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'

db = SQLAlchemy(app)

# 检查数据库是否连接成果
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("SELECT 1"))
        print(rs.fetchone())  # (1,)
```

### 创建ORM对象
通过创建ORM模型对象，在数据库中创建一个表
```
class User_ORM(db.Model):
    # 表名
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
# 之后将这个表映射到数据库中
with app.app_context():
    db.create_all()
```


### ORM实现增删改查 CRUD
#### 增
```
@app.route('/user/add')
def add_user():
    user1 = User_ORM(username="msy", password="msyhs233")

    # 向数据库中添加一个信息
    db.session.add(user1)
    db.session.commit()

    return "对象创建成功"
```

#### 删
```
@app.route('/user/delete')
def delete_user():
    user = User_ORM.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "数据删除成功"

```

#### 改
```
@app.route('/user/update')
def update_user():
    user = User_ORM.query.filter_by(username="msy")[0]
    user.password = "222222"
    db.session.commit()

    return "数据修改成功"

```

#### 查
```
@app.route('/user/query')
def query_user():
    # 有两种查询方式
    # get: 根据primary key进行查找
    user = User_ORM.query.get(1)
    print(user.username)
    
    
    # filter:
    # 返回的是QuerySet对象
    users = User_ORM.query.filter_by(username="msy")
    for user in users:
        print(user.username)

    return "数据查找成功"

```        




### ORM实现表关系
外键实现表的连接, 以现在的User和Article为例子

```
class User_ORM(db.Model):
    # 表名和类名有什么区别
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    articles = db.relationship("Article", back_populates="author")
    

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User_ORM", back_populates="articles")
    

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
    
```


### 将ORM模型映射到数据库
```
# 之后将这个表映射到数据库中
with app.app_context():
    db.create_all()
```
之前使用的方式, 当一个ORM对象中的特征发生改变时, 对应的数据库中的表不会发生改变, 所以要使flask-migrate

在app.py中:
```
db = SQLAlchemy(app)

migrate = Migrate(app, db)
```

在terminal中 (要记得到app.py存在的文件目录下)
```
flask db init #只需要运行一次

flask db migrate

flask db upgrade

```









