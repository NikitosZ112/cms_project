from django.db import models
from polymorphic.models import PolymorphicModel

class Content(PolymorphicModel):
    title = models.CharField(max_length=255, verbose_name="Заголовок", help_text="Заголовок контента")
    counter = models.PositiveIntegerField(default=0, verbose_name="Счетчик просмотров",
                                          help_text="Автоматически увеличивается при просмотре страницы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_real_instance_class().__name__})"

class Video(Content):
    video_file_url = models.URLField(verbose_name="Ссылка на видеофайл", help_text="URL видеофайла")
    subtitle_file_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на файл субтитров",
                                        help_text="URL файла субтитров (опционально)")

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

class Audio(Content):
    text_content = models.TextField(verbose_name="Текстовое содержимое", help_text="Текст произвольной длины, связанный с аудио")

    class Meta:
        verbose_name = "Аудио"
        verbose_name_plural = "Аудио"
