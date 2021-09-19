from django.db import models
from django.conf import settings
import random
from django.db import models

User = settings.AUTH_USER_MODEL
# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.FileField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.content)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 100),
            "dislikes": random.randint(0, 20),
        }
