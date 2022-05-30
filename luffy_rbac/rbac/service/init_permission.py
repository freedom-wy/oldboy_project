from django.conf import settings
from utils.log import logger


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user: 当前用户对象
    :param request: 请求相关所有数据
    :return:
    """
    # 2. 权限信息初始化
    # 根据当前用户信息获取此用户所拥有的所有权限，并放入session。
    # 当前用户所有权限
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__url",
                                                                                      "permissions__title",
                                                                                      "permissions__menu_id",
                                                                                      "permissions__menu__title",
                                                                                      "permissions__menu__icon"
                                                                                      ).distinct()
    permission_list = []
    menu_dict = {}

    """
        {'permissions__id': 1, 'permissions__url': '/customer/list/', 'permissions__title': '客户列表', 'permissions__menu_id': 2, 'permissions__menu__title': '用户管理', 'permissions__menu__icon': 'fa fa-bathtub'}
        {'permissions__id': 2, 'permissions__url': '/customer/add/', 'permissions__title': '增加客户', 'permissions__menu_id': None, 'permissions__menu__title': None, 'permissions__menu__icon': None}
        {'permissions__id': 3, 'permissions__url': '/customer/list/(?P<cid>\\d+)/', 'permissions__title': '删除客户', 'permissions__menu_id': None, 'permissions__menu__title': None, 'permissions__menu__icon': None}
        {'permissions__id': 4, 'permissions__url': '/customer/edit/(?P<cid>\\d+)/', 'permissions__title': '修改客户', 'permissions__menu_id': None, 'permissions__menu__title': None, 'permissions__menu__icon': None}
        {'permissions__id': 5, 'permissions__url': '/payment/list/', 'permissions__title': '订单列表', 'permissions__menu_id': 1, 'permissions__menu__title': '信息管理', 'permissions__menu__icon': 'fa fa-bathtub'}
        {'permissions__id': 6, 'permissions__url': '/payment/add/', 'permissions__title': '添加订单', 'permissions__menu_id': None, 'permissions__menu__title': None, 'permissions__menu__icon': None}
        {'permissions__id': 7, 'permissions__url': '/payment/edit/(?P<pid>\\d+)/', 'permissions__title': '编辑订单', 'permissions__menu_id': None, 'permissions__menu__title': None, 'permissions__menu__icon': None}
        {'permissions__id': 8, 'permissions__url': '/payment/del/(?P<pid>\\d+)/', 'permissions__title': '删除订单', 'permissions__menu_id': None, 'permissions__menu__title': None, 'permissions__menu__icon': None}
    """

    for item in permission_queryset:
        permission_list.append(item['permissions__url'])

        menu_id = item['permissions__menu_id']
        if not menu_id:
            continue
        node = {'title': item['permissions__title'], 'url': item['permissions__url']}
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node, ]
            }
    """
        {2: {'title': '用户管理', 'icon': 'fa fa-bathtub', 'children': [{'title': '客户列表', 'url': '/customer/list/'}]}, 1: {'title': '信息管理', 'icon': 'fa fa-bathtub', 'children': [{'title': '订单列表', 'url': '/payment/list/'}]}} 
    """
    logger.info("用户: {}， 权限列表: {}".format(current_user, permission_list))
    logger.info("用户: {}, 菜单数据: {}".format(current_user, menu_dict))
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict

