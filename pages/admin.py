from django.contrib import admin
from .models import Page, PageContent
from content.models import Content

class PageContentInline(admin.TabularInline):
    model = PageContent
    extra = 1
    fields = ('content', 'order')
    ordering = ('order',)
    autocomplete_fields = ('content',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content":
            kwargs["queryset"] = Content.objects.all().order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [PageContentInline]
    list_display = ('title', 'get_content_count', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Основная информация', {'fields': ('title',)}),
        ('Служебная информация', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def get_content_count(self, obj):
        return obj.pagecontent_set.count()
    get_content_count.short_description = "Количество контента"

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('page', 'content', 'order', 'get_content_type')
    list_filter = ('page', 'content__polymorphic_ctype')
    search_fields = ('page__title', 'content__title')
    list_editable = ('order',)
    ordering = ('page', 'order')
    autocomplete_fields = ('page', 'content')

    def get_content_type(self, obj):
        return obj.content.get_real_instance_class().__name__
    get_content_type.short_description = "Тип контента"
