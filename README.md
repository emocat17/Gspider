![Build](https://github.com/Gerapy/Gerapy)

# 1、克隆项目
```sh
git clone https://github.com/Gerapy/Gerapy.git  # 如果直接clone失败可以下载zip代码压缩包
```

# 2、安装依赖
```sh
pip install -r requirements.txt
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple  # 镜像安装
```

# 3、本地运行
```sh
python manage.py # 查看支持参数
python manage.py migrate  # 初始化数据库
python manage.py createsuperuser  # 创建超级管理员
```

# 4、目录结构
- scrapydData : 存储scrapyd数据
- projects ： 存储Gerapy新增的项目数据

# 5、运行服务1
```sh
python manage.py runserver  # 启动服务：终端1
scrapyd # 终端2
```

# 5、运行服务2
```sh
cd scrapydData
scrapyd # 运行scrapyd-client服务
```


# 6、前端依赖
- 前提是安装nodejs 
```sh
cd gerapy/client
npm install -g pnpm
pnpm install 
```

