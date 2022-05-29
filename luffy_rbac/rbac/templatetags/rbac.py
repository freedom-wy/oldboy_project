from django.template import Library
from django.conf import settings
import re

register = Library()


@register.inclusion_tag("rbac/menu.html")
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    for item in menu_list:
        reg = "^{}$".format(item.get("url"))
        if re.match(reg, request.path_info):
            item["active"] = "active"
    return {"menu_list": menu_list}
