from celery import shared_task
from django.db import transaction
from django.db.models import F
from content.models import Content

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def increment_content_counters(self, content_ids):
    try:
        with transaction.atomic():
            updated_count = Content.objects.filter(id__in=content_ids).update(counter=F('counter') + 1)
            return {
                'status': 'success',
                'updated_count': updated_count,
                'content_ids': content_ids
            }
    except Exception as exc:
        print(f"Ошибка при обновлении счетчиков: {exc}")
        raise self.retry(exc=exc)
