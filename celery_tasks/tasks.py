from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
app = Celery('celery_tasks.tasks',broker='redis://192.168.0.118:6380/8')

@app.task
def send_register_active_email(to_email,username,token):
    subject = 'eb购物'
    message ='messageda'
    sender = settings.EMAIL_FROM
    receiver =[to_email]
    html_message = '<h1>%s,欢迎你成为eb购物的成员</h1>请点击链接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username,token,token)
    send_mail(subject,message,sender,receiver,html_message=html_message)
