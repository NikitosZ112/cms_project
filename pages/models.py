from django.db import models
from content.models import Content

class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок страницы", help_text="Заголовок страницы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_ordered_content(self):
        return Content.objects.filter(pagecontent__page=self).order_by('pagecontent__order')

class PageContent(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name="Страница")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name="Контент")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок",
                                        help_text="Порядок отображения контента на странице (меньшее число = выше)")

    class Meta:
        verbose_name = "Контент страницы"
        verbose_name_plural = "Контент страниц"
        ordering = ['order']
        unique_together = ['page', 'content']

    def __str__(self):
        return f"{self.page.title} - {self.content.title} ({self.order})"
