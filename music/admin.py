from django.contrib import admin
from django.utils.html import mark_safe

from .models import Genre, Tag, Track, TrackDetails


admin.site.site_header = 'Музыкальный каталог — администрирование'
admin.site.site_title = 'Музыкальный каталог'
admin.site.index_title = 'Управление записями'


class HasDetailsFilter(admin.SimpleListFilter):
    title = 'детали трека'
    parameter_name = 'has_details'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'С деталями'),
            ('no', 'Без деталей'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(details__isnull=False)
        if self.value() == 'no':
            return queryset.filter(details__isnull=True)
        return queryset


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'genre',
        'release_year',
        'duration',
        'duration_minutes',
        'tag_list',
        'play_count',
        'is_published',
        'image_preview',
    )
    list_editable = ('play_count', 'is_published')
    list_filter = ('is_published', 'genre', 'release_year', HasDetailsFilter)
    search_fields = ('title', 'slug')
    ordering = ('-release_year', 'title')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    actions = ('mark_published', 'reset_play_count')
    fieldsets = (
        ('Основная информация', {'fields': ('title', 'slug', 'genre', 'tags')}),
        (
            'Параметры трека',
            {
                'fields': (
                    'duration',
                    'release_year',
                    'play_count',
                    'is_published',
                )
            },
        ),
        ('Медиа', {'fields': ('image', 'image_preview')}),
        ('Справочная информация', {'classes': ('collapse',), 'fields': ('duration_minutes_display',)}),
    )
    readonly_fields = ('duration_minutes_display', 'image_preview')

    @admin.display(description='Теги')
    def tag_list(self, obj):
        names = list(obj.tags.values_list('name', flat=True))
        return ', '.join(names) if names else '—'

    @admin.display(description='Длительность, мин')
    def duration_minutes(self, obj):
        return round(obj.duration / 60, 2)

    @admin.display(description='Длительность (мин)')
    def duration_minutes_display(self, obj):
        if not obj or not obj.pk:
            return '—'
        return self.duration_minutes(obj)

    @admin.display(description='Обложка')
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="80" height="80" style="object-fit:cover;border-radius:4px;" />')
        return '—'

    @admin.action(description='Отметить выбранные треки как опубликованные')
    def mark_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'Обновлено {updated} трек(ов).')

    @admin.action(description='Сбросить счётчик прослушиваний')
    def reset_play_count(self, request, queryset):
        updated = queryset.update(play_count=0)
        self.message_user(request, f'Сброшено прослушиваний у {updated} трек(ов).')

    class Media:
        css = {'all': ('music/css/admin.css',)}


@admin.register(TrackDetails)
class TrackDetailsAdmin(admin.ModelAdmin):
    list_display = ('track', 'lyrics_author', 'bpm', 'has_video')
