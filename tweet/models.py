from django.db import models
import random
# Create your models here.


class Tweet(models.Model):
    content = models.TextField()
    image = models.FileField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.content)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 100),
            "dislikes": random.randint(0, 20),
        }
