from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
#from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    #image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        #img = Image.open(self.image.path)

        #if img.height > 300 and img.width > 300:
            #img.save(self.image.path, optimize = True, quality = 10)

      
class UserTimer(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    timers = models.CharField(max_length=500)
    display_order = models.IntegerField(null=False, db_column='display_order')

    class Meta:
        unique_together= (('user', 'timers'),)
        
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
