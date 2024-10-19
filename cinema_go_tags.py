from django import template
from cinema_go.models import Category


register = template.Library()  # Создаём декоратер

@register.simple_tag()  # Декоратер позволит вызывать функцию в html
def get_categories():
    return Category.objects.all()






