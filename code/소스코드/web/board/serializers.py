from board.models import Message, Comment
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.userid')
    # created_at = serializers.DateTimeField(format="%Y년 %m월 %d일")
    class Meta:
        model = Message
        fields = ['id', 'title', 'created_at', 'user', 'content']
        ordering = ['-id']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.userid')
    message = serializers.ReadOnlyField(source = 'message.id')
    # created_at = serializers.DateField(format="%Y년 %m월 %d일")
    class Meta:
        model = Comment
        fields = ['id', 'message', 'user', 'created_at', 'content']
        ordering = ['-id']