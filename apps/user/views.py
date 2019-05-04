from django.shortcuts import render
from django.http import HttpResponse
import re
from django.views.generic import View
from user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
#如果密钥过期会有下面的异常
from itsdangerous import SignatureExpired
#发送邮件包
from django.core.mail import send_mail
import time
from celery_tasks.tasks import send_register_active_email
#系统自带的 认证和登录 
from django.contrib.auth import authenticate,login

# Create your views here.


 
# def register(request):
# 	if request.method =='GET':
# 		return render(request,'register.html')
# 	else:
# 		pass
# def my_register(request):
# 	return render(request,'my_register.html')
# def register_handle(request):
#     username = request.POST.get('user_name')
#     password = request.POST.get('pwd')
#     email = request.POST.get('email')
#     allow = request.POST.get('allow')
#     #进行数据的验证

#     # 返回应答, 跳转到首页
#     return HttpResponse('ok')

class RegisterView(View):
	def get(self,request):
		return render(request,'my_register.html')

	def post(self,request):
		#接受数据
		username = request.POST.get('user_name')
		password = request.POST.get('pwd')
		cpassword = request.POST.get('cpwd')
		email = request.POST.get('email')
		allow = request.POST.get('allow')
        #数据验证
		if not all([username,password,email,allow]):
			return render(request,'my_register.html',{'errmsg':'数据不能为空'})
		if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
			return render(request,'my_register.html',{'errmsg':'请输入正确的邮箱'})
		if allow!='on':
			return render(request,'my_register.html',{'errmsg':'请同意协议'})
		if password!= cpassword:
			return render(request,'my_register.html',{'errmsg':'请重新确认密码'})
		#检查用户是否存在
		try:
		    user =User.objects.get(username=username)
		except User.DoesNotExist:
			user = None
		if user:
			return render(request,'my_register.html',{'errmsg':'用户名已存在'})

		#数据库创建数据
		user = User.objects.create_user(username,email,password)
		user.is_active=0
		user.save()
		#发送激活链接，http://127.0.0.1:8000/user/active/加密的身份信息
		#加密身份信息
		serializer = Serializer(settings.SECRET_KEY,3600)
		info ={'confirm':user.id}
		token = serializer.dumps(info)
		token= token.decode()

		#发送邮件,主题，正文，发件人，收件人列表
		# subject = 'eb购物'
		# message ='messageda'
		# sender = settings.EMAIL_FROM
		# receiver =[email]
		# html_message = '<h1>%s,欢迎你成为eb购物的成员</h1>请点击链接激活你的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username,token,token)
		# send_mail(subject,message,sender,receiver,html_message=html_message)
		#改用celery redis 加入任务 ，
		send_register_active_email.delay(email,username,token)
		print(username)
  
		return HttpResponse('okfas') 


class ActiveView(View):
	def get(self,request,token):
		'''对token进行解密'''
		serializer = Serializer(settings.SECRET_KEY,3600)
		try:
			info=serializer.loads(token)
			user_id = info['confirm']
			user= User.objects.get(id = user_id)
			user.is_active=1;
			user.save()
			#激活成功，返回登录界面
			#return redirect(reverse('user:login'))
			return HttpResponse('激活成功')

		except SignatureExpired :
		 	return HttpResponse('激活链接已过期')


class LoginView(View):
	def get(self,request):
		return render(request,'login.html')
	def post(self,request):
		#接受数据
		username = request.POST.get('user_name')
		password = request.POST.get('pwd')
		#登录校验
		if not all([username,password]):
			return render(request,'loign.html',{'errmsg':'数据不完整'})
		user =authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				#记录登录状态,django的login函数
				login(request,user)
				return redirect(reverse('goods:index'))
			else:
			 	return render(request,'login.html',{'errmsg':'帐号未激活'})

		else:
		 	return render(request,'login.html',{'errmsg':'帐号或密码不正确'})

			#return render(request,'login.html'，{'errmsg':'帐号或密码不正确'})


		#返回应答  
