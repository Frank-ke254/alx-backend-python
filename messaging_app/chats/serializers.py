from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    class Meta:
        model = User
        exclude = ["password", "user_permissions", "groups"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password) 
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ["uuid", "sender", "sender_email", "message_body", "sent_at"]

    def get_sender_email(self, obj):
        return obj.sender.email if obj.sender else None

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    title = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Conversation
        fields = ["uuid", "participants", "created_at", "messages", "title"]

    def validate_title(self, value):
        if value and len(value) < 3:
            raise serializers.ValidationError("Title too short!")
        return value
