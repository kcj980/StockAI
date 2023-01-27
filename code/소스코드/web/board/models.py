from django.db import models
from django.conf import settings
from accounts.models import Userdata

# Create your models here.
class Message(models.Model):
  id = models.AutoField(primary_key=True, null=False, blank=False, db_column='message_id')
  title = models.CharField(max_length=100, db_column='title')
  content = models.TextField(db_column='content')
  created_at = models.DateField(auto_now_add=True, db_column='date_time')
  user = models.ForeignKey(Userdata, null=True, blank=True, on_delete=models.CASCADE, db_column='userid')

  class Meta:
        managed = False
        db_table = 'message'

class Comment(models.Model):
  id = models.AutoField(primary_key=True, null=False, blank=False, db_column='comment_id')
  message = models.ForeignKey(Message, null=False, blank=False, on_delete=models.CASCADE, db_column='message_id')
  user = models.ForeignKey(Userdata, null=False, blank=False, on_delete=models.CASCADE, db_column='userid')
  created_at = models.DateField(auto_now_add=True, null=False, blank=False, db_column='date_time')
  content = models.TextField(db_column='content')
  
  class Meta:
        managed = False
        db_table = 'comment'
