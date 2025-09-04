from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from .models import Content, Video, Audio

class ContentChildAdmin(PolymorphicChildModelAdmin):
    base_model = Content
    readonly_fields = ('counter', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
    list_display = ('title', 'counter', 'created_at')

@admin.register(Video)
class VideoAdmin(ContentChildAdmin):
    base_model = Video
    fieldsets = (
        ('Основная информация', {'fields': ('title',)}),
        ('Видео данные', {'fields': ('video_file_url', 'subtitle_file_url')}),
        ('Статистика', {'fields': ('counter', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    list_display = ('title', 'video_file_url', 'counter', 'created_at')

@admin.register(Audio)
class AudioAdmin(ContentChildAdmin):
    base_model = Audio
    fieldsets = (
        ('Основная информация', {'fields': ('title',)}),
        ('Аудио данные', {'fields': ('text_content',)}),
        ('Статистика', {'fields': ('counter', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    list_display = ('title', 'get_text_preview', 'counter', 'created_at')

    def get_text_preview(self, obj):
        return obj.text_content[:50] + "..." if len(obj.text_content) > 50 else obj.text_content
    get_text_preview.short_description = "Текст (превью)"

@admin.register(Content)
class ContentParentAdmin(PolymorphicParentModelAdmin):
    base_model = Content
    child_models = (Video, Audio)
    search_fields = ('title',)
    list_display = ('title', 'get_content_type', 'counter', 'created_at')
    list_filter = ('polymorphic_ctype', 'created_at')

    def get_content_type(self, obj):
        return obj.get_real_instance_class().__name__
    get_content_type.short_description = "Тип контента"
