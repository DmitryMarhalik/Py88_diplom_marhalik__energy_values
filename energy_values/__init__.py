from energy_values.celery_setup import app as celery_app

#  Загрузка приложения Celery при запуске Django гарантирует,
#  что декоратор @shared_task будет использовать его правильно

__all__ = ("celery_app",)
