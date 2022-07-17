from pyexpat import model
from django.db import models

# Create your models here.

class Chatbot(models.Model):

    unidentifiedText = models.TextField(blank=True)


    def __str__(self):
        return str(self.unidentifiedText)

