### rbac
#### 1、创建rbac应用
#### 2、创建rbac模型类
```python
# 权限表
class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name="标题", max_length=32)
    url = models.CharField(verbose_name="含正则的URL", max_length=128)
    is_menu = models.BooleanField(verbose_name="是否可做菜单", default=False)
    icon = models.CharField(verbose_name="菜单图标", max_length=32, null=True, blank=True)

    def __str__(self):
        return self.title

# 2、角色表
class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name="角色名称", max_length=32)
    permissions = models.ManyToManyField(verbose_name="拥有的所欲权限", to="Permission", blank=True)

    def __str__(self):
        return self.title

# 3、用户信息表
class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    email = models.CharField(verbose_name="邮箱", max_length=32)
    roles = models.ManyToManyField(verbose_name="拥有的所有角色", to=Role, blank=True)

    def __str__(self):
        return self.name
```
#### 3、在settings中添加应用
#### 4、执行迁移
#### 5、录入数据
#### 6、登录时通过用户信息查询该用户拥有的权限
```python
permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__url",
                                                                                      "permissions__is_menu",
                                                                                      "permissions__title",
                                                                                      "permissions__icon"
                                                                                      ).distinct()
# 获取权限中所有的URL
permission_list = []
menu_list = []
for item in permission_queryset:
    permission_list.append(item['permissions__url'])
    if item["permissions__is_menu"]:
        menu_list.append(
            {
                "title": item.get("permissions__title"),
                "icon": item.get("permissions__icon"),
                "url": item.get("permissions__url")
            }
        )
logger.info("用户: {}, 权限列表: {}, 菜单列表: {}".format(current_user.name, permission_list, menu_list))
request.session[settings.PERMISSION_SESSION_KEY] = permission_list
request.session[settings.MENU_SESSION_KEY] = menu_list
```
#### 7、在中间件中进行校验
```python
class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入时候出发执行
        :param request:
        :return:
        """

        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """
        # 获取请求的URL
        current_url = request.path_info
        logger.info("当前访问路径为: {}".format(current_url))
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None

        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_list:
            return HttpResponse('未获取到用户权限信息，请登录！')

        flag = False

        for url in permission_list:
            reg = "^%s$" % url
            if re.match(reg, current_url):
                flag = True
                break

        if not flag:
            return HttpResponse('无权访问')
```

