import os
from celery import Celery

# Задаём переменную окружения, содержащую название файла настроек нашего проекта
# для консольных команд celery
project_name = 'shop'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')

# создаём экземпляр приложения
app = Celery('shop')

# загружаем конфигурацию из настроек нашего проекта
# namespace='CELERY' - префикс, который мы будем использовать
# для всех настроек связанных с celery
# т.е. в django settings можно использовать константы CELERY_<SOME_WORD>
# типо CELERY_BROKER_URL
app.config_from_object('django.conf:settings', namespace='CELERY')

# вызываем процесс поиска и загрузки асинзронных задач
# celery пройдёт по всем приложениям, из INSTALLED_APPS
# и попытается найти файл tasks.py, чтобы запустить код задач
app.autodiscover_tasks()
