from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import UserActivityLog
from django.utils import timezone

@receiver(user_logged_in)
def create_user_login_log(sender, request, user, **kwargs):
    UserActivityLog.objects.create(user=user, login_time=timezone.now())

@receiver(user_logged_out)
def update_user_logout_log(sender, request, user, **kwargs):
    last_log = UserActivityLog.objects.filter(user=user, logout_time__isnull=True).last()
    if last_log:
        last_log.logout_time = timezone.now()
        last_log.save()