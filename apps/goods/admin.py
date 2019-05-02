from django.contrib import admin

# Register your models here.
from goods.models import GoodsType,IndexPromotionBanner,GoodsSKU,IndexGoodsBanner,IndexTypeGoodsBanner

class GoodsType_admin(admin.ModelAdmin):
	list_display=['name']
admin.site.register(GoodsType,GoodsType_admin)

class IndexPromotionBanner_admin(admin.ModelAdmin):
	list_display=['name']
admin.site.register(IndexPromotionBanner,IndexPromotionBanner_admin)

class GoodsSKU_admin(admin.ModelAdmin):
	list_display=['name']
admin.site.register(GoodsSKU,GoodsSKU_admin)

