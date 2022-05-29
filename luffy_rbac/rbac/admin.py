from django.contrib import admin
from .models import Permission, UserInfo, Role

admin.site.register(Permission)
admin.site.register(UserInfo)
admin.site.register(Role)

