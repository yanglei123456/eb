1 eb购物平台的搭建主要用到以下工具
python3.6 
django1.8.2 
pymysql 主要存储库
celcery3.1.0 耗时任务发邮件
biliiard3.3.0.23
django-tinymce2.6.0 
redis3.2.1 进行耗时任务发邮件
itsdangerous1.1.0加密处理
1.1数据库的创建，平台搭建
2.1 往虚拟机中copy一份代码，在celery_tasks中的tasks.py中添加初始化和django设置，内容如下
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eb.settings")
django.setup()
并且在虚拟机中装入celery==3.1.26  django-celery==3.2.2 django==1.8.2 redis==2.10.6
redis版本高会导致str错误。
2.2 虚拟机中的主机装mysql，redis 并且要在python3运行。
3.1 redis存储session