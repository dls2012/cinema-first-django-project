from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Cinema, Comment, Profile, City, Ip

# Register your models here.
# Здесь регистрируются модели что бы они отображались в Админке
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(City)
admin.site.register(Ip)
# admin.site.register(Cinema)

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'get_image')
    list_display_links = ('id', 'title')
    list_filter = ('category',)
    list_editable = ('category',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75"> ')
        else:
            return '-'

    get_image.short_description = 'Картинка'

