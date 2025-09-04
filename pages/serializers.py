from rest_framework import serializers
from .models import Page
from content.models import Content, Video, Audio

class ContentSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'counter', 'content_type', 'created_at', 'updated_at']

    def get_content_type(self, obj):
        return obj.get_real_instance_class().__name__

    def to_representation(self, instance):
        real_instance = instance.get_real_instance()
        data = super().to_representation(instance)

        if isinstance(real_instance, Video):
            data['video_file_url'] = real_instance.video_file_url
            data['subtitle_file_url'] = real_instance.subtitle_file_url
        elif isinstance(real_instance, Audio):
            data['text_content'] = real_instance.text_content

        return data

class PageListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'created_at', 'detail_url']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/pages/{obj.id}/')
        return f'/api/pages/{obj.id}/'

class PageDetailSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'created_at', 'updated_at', 'content']

    def get_content(self, obj):
        ordered_content = obj.get_ordered_content()
        return ContentSerializer(ordered_content, many=True, context=self.context).data
