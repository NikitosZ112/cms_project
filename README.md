# Django CMS Project

Backend CMS на Django для страниц с видео- и аудиоконтентом.  
Поддержка масштабируемых связей, онлайн-счетчиков просмотров, REST API и админки.

## Установка и запуск
```bash
git clone https://github.com/NikitosZ112/cms_project.git
cd cms_project
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate в Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Redis и Celery для фоновых задач (Windows)
```bash
redis-server
celery -A cms_project worker --loglevel=info -P threads```
```

## Основной функционал
Страницы с произвольным количеством видео/аудио
REST API: /api/pages/ (список), /api/pages/<id>/ (детали)
Счетчики просмотров обновляются асинхронно
Админка с поиском и inline-редактированием
