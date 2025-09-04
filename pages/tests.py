from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from .models import Page, PageContent
from content.models import Video, Audio

class PageAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.page1 = Page.objects.create(title="Первая страница")
        self.page2 = Page.objects.create(title="Вторая страница")
        self.page3 = Page.objects.create(title="Третья страница")

        self.video = Video.objects.create(
            title="Тестовое видео",
            video_file_url="https://example.com/video.mp4",
            subtitle_file_url="https://example.com/subtitles.srt"
        )

        self.audio = Audio.objects.create(
            title="Тестовое аудио",
            text_content="Это длинный текст для аудио контента..."
        )

        PageContent.objects.create(page=self.page1, content=self.video, order=1)
        PageContent.objects.create(page=self.page1, content=self.audio, order=2)

class PageListAPITest(PageAPITestCase):
    def test_get_pages_list_success(self):
        url = reverse('pages:page-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 3)

class PageDetailAPITest(PageAPITestCase):
    @patch('pages.tasks.increment_content_counters.delay')
    def test_get_page_detail_success(self, mock_task):
        url = reverse('pages:page-detail', kwargs={'pk': self.page1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('content', response.data)
        mock_task.assert_called_once()
