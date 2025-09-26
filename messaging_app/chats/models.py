import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255, null=False)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.email} ({self.role})"
    
class Conversation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.id}"
    
class Message(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    converstion = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(timezone.now)
    created_at = models.DateTimeField(timezone.now)

    def __str__(self):
        return f"Message {self.id} from {self.sender.email}"
