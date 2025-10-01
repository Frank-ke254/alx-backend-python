from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="abc123")
        self.receiver = User.objects.create_user(username="receiver", password="def123")

    def test_message_creates_notification(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.receiver)
        self.assertFalse(notification.is_read)
