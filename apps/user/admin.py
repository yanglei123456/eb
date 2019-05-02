from django.contrib import admin
from user.models import User


# Register your models here.
class User_admin(admin.ModelAdmin):
	list_display=['username','create_time','update_time']

admin.site.register(User,User_admin)