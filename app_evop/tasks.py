from time import sleep
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from celery import shared_task
from django.conf import settings


@shared_task()
def send_email_task(user_email, message):
    """
    Sends an email when the feedback or add-food form has been submitted.
    """

    sleep(20)  # Simulate expensive operation(s) that freeze Django
    try:
        send_mail('EVOP app',
                  message=message,
                  from_email=user_email,
                  recipient_list=[settings.EMAIL_HOST_USER],
                  )
    except BadHeaderError:
        return HttpResponse('Incorrect header found')  # BadHeaderError, чтобы предотвратить вставку злоумышленниками
# # дополнительных заголовков электронной почты. Если обнаружен “плохой заголовок”,
# # то представление вернет клиенту HttpResponse с текстом “Incorrect header found”.
