from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from task_manager.models import Task

# Словарь для хранения предыдущих статусов, чтобы не отправлять повторно
PREVIOUS_STATUSES = {}

@receiver(pre_save, sender=Task)
def notify_task_status_change(sender, instance, **kwargs):
    if not instance.pk:
        # Новая задача, уведомлять не нужно
        return

    try:
        previous = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    old_status = previous.status
    new_status = instance.status

    # Проверка: статус изменился и email ещё не отправлялся для этого изменения
    key = f"{instance.pk}-{new_status}"
    if old_status != new_status and key not in PREVIOUS_STATUSES:
        PREVIOUS_STATUSES[key] = True

        subject = f"Task '{instance.title}' updated"
        message = f"Hello {instance.owner.username},\n\n" \
                  f"Your task '{instance.title}' has changed status from '{old_status}' to '{new_status}'."

        send_mail(
            subject,
            message,
            None,  # from_email возьмется из DEFAULT_FROM_EMAIL
            [instance.owner.email],
            fail_silently=False,
        )
