from django.contrib import admin
from .models import Permission, UserInfo, Role, Menu

# class CityAdmin(admin.ModelAdmin):
#     # 在管理后台中搜索
#     search_fields = ["name", "desc"]
#     # 在管理后台中过滤
#     list_filter = ["name", "desc", "add_time"]
#     list_display = ['name', 'desc', 'add_time']


class PermissionAdmin(admin.ModelAdmin):
    """
    在admin中显示字段
    """
    list_display = ["title", "url"]


admin.site.register(Menu)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(UserInfo)
admin.site.register(Role)
