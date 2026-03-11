from django import template

from music.views import SECTIONS

register = template.Library()


@register.simple_tag
def get_music_sections_count():
    """Возвращает количество разделов музыкального каталога."""
    return len(SECTIONS)


@register.inclusion_tag('music/tags/sections.html')
def show_music_sections():
    """Выводит список ключевых разделов каталога через отдельный шаблон."""
    return {'sections': SECTIONS}
