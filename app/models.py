from django.db import models

# Create your models here.

class Client(models.Model):
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    
    def __str__(self):
        return self.username
    
    
class UserSong(models.Model):
    music = models.FileField(upload_to='media')
    
    def __str__(self):
        return self.music