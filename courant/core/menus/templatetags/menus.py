from django.template import Library, Node, Variable, TemplateSyntaxError
from django.conf import settings

from courant.core.utils.text import split_contents
from courant.core.menus.models import MenuLocation, Menu, MenuItem

register = Library()

class GetMenuNode(Node):
    def __init__(self, location_name, varname):
        self.location_name = location_name
        self.varname = varname
        
    def render(self, context):
        path = context['request'].path
        location = MenuLocation.objects.get(name=Variable(self.location_name).resolve(context))
        menu = location.menu_for_page(path)
        if menu:
            items = MenuItem.objects.filter(menu=menu)
            obj = {'menu': menu, 'items': items, 'active_item': menu.item_for_page(path)}
            context[self.varname] = obj
        return ''

def do_menu(parser, token):
    """
    Determines the correct menu to show for the location.
    
    Syntax::
    
        {% get_menu [MenuLocation] as [varname] %}
    
    Sample usage::
    
        {% get_menu "MainNavigation" as main_nav %}
        <ul>
        {% for item in main_nav.items %}
            <li {% ifequal item main_nav.active_item %}class="active"{% endifequal %}>
                <a href="{{ item.active_url }}">{{ item.name }}</a>
            </li>
        {% enfor %}
        </ul>
    """
    bits = split_contents(token)
    
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_menu: invalid syntax"
    
    return GetMenuNode(bits[1], bits[3])
register.tag('get_menu', do_menu)