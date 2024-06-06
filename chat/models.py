from django.db import models
from django.utils.text import slugify
from authentication.models import User
import os

class ChatRoom(models.Model):
	type = models.CharField(max_length=2 , default='dm' )
	name = models.CharField(max_length=50 ,unique=True, blank=True)
	member = models.ManyToManyField(User)
	last_update = models.DateTimeField(auto_now=True)
	
	def save(self, *args, **kwargs):
		 # Save the ChatRoom instance to the database to get an ID
		super().save(*args, **kwargs)
		# Now that the ID is set, you can use the many-to-many relationship
		users = ""
		for usr in self.member.all():
			users += usr.username+", "
		self.name = slugify(users)
		super(ChatRoom, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class VideoCall(models.Model):
	room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
	caller = models.ForeignKey(User , on_delete=models.CASCADE)
	is_active = models.BooleanField(default=False)
	def __str__(self):
		return self.room.name

class BaseMessage(models.Model):
	user  = models.ForeignKey(User , verbose_name='Sender' ,on_delete=models.SET_NULL , null=True)
	room = models.ForeignKey(ChatRoom , on_delete=models.CASCADE,related_name='%(app_label)s_%(class)s_related')
	timestamp = models.DateTimeField(auto_now_add=True)
	read = models.BooleanField(default=False)

	class Meta:
		abstract = True

class ChatMessage(BaseMessage):
	content = models.CharField(max_length=255)
	def __str__(self):
		return self.content
	

def audio_upload_path(instance, filename):
    room_name = f'room_{instance.room.name}'
    return os.path.join('chats', room_name, 'audios' ,filename)

class AudioVideo(BaseMessage):
	file = models.FileField(upload_to= audio_upload_path)


	
"""
In the BaseMessage model, the related_name value is set to '%(app_label)s_%(class)s_related'. This is a dynamic value that will be replaced with the actual app label and class name when the model is used.

In this case, %(app_label)s will be replaced with the lowercase version of the app label where the model is defined, and %(class)s will be replaced with the lowercase name of the model class itself.

For example, if the BaseMessage model is defined in an app with the label "chat" and is being used by the ChatMessage model, the related_name value will be 'chat_chatmessage_related'.

This dynamic related_name value helps to avoid clashes in reverse relations when multiple models inherit from BaseMessage within the same app.

Note that when using this dynamic related_name value, you won't need to explicitly specify the related_name in the ChatMessage and AudioVideo models. The dynamic value defined in BaseMessage will be used for their reverse relations with ChatRoom
"""