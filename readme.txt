2.1 往虚拟机中copy一份代码，在celery_tasks中的tasks.py中添加初始化和django设置，内容如下
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eb.settings")
django.setup()
并且在虚拟机中装入celery==3.1.26  django-celery==3.2.2 django==1.8.2 redis==2.10.6
redis版本高会导致str错误。
2.2 虚拟机中的主机装mysql，redis 并且要在python3运行。