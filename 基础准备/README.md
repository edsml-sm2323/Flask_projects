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

图片: <img> </img>

css文件: <link> </link>

Javascript文件: <script> </script>


## 数据库连接
ORM模型：对象关系映射 不用SQL语句 一个ORM模型与数据库中的一张表对应

### 创建ORM对象


### ORM实现增删改查 CRUD


### ORM实现表关系

### 将ORM模型映射到数据库








