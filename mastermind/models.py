from django.db import models

# Create your models here.
class Game(models.Model):
    def __str__(self):
        return "GamedId: {}".format(self.id)

