from django.template import Library
from django.conf import settings

register = Library()


@register.inclusion_tag("menu.html")
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    return {"menu_list": menu_list}
