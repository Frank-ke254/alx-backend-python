from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

User = get_user_model()


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    Notification.objects.filter(user=instance).delete()
    messages = Message.objects.filter(sender=instance) | Message.objects.filter(receiver=instance)
    for msg in messages:
        msg.delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
