from rest_framework import generics
from rest_framework.response import Response

from .models import Page
from .serializers import PageListSerializer, PageDetailSerializer
from .tasks import increment_content_counters

class PageListView(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer

    def get_queryset(self):
        return Page.objects.all().order_by('-created_at')

class PageDetailView(generics.RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        content_ids = list(instance.get_ordered_content().values_list('id', flat=True))
        serializer = self.get_serializer(instance)
        if content_ids:
            increment_content_counters.delay(content_ids)
        return Response(serializer.data)

    def get_queryset(self):
        return Page.objects.prefetch_related('pagecontent_set__content').all()
