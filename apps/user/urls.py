

from django.conf.urls import url
# from user import views
from user.views import RegisterView,ActiveView,LoginView
urlpatterns = [
   # url(r'^register$',views.register,name='register'),
   # url(r'^my_register$',views.my_register,name='my_register'),
   # url(r'^register_handle',views.register_handle,name='register_handle'),下面改用类视图的url
   url(r'^my_register$',RegisterView.as_view(),name='my_register'), 
   url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'), 
   url(r'^login$',LoginView.as_view(),name='login'), 
]
