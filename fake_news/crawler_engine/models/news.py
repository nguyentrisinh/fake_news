import json
from django.db import models
from django.utils import timezone


class NewsItem(models.Model):
    link = models.TextField(default="")  # this stands for our crawled data
    description = models.TextField(default="")
    title = models.TextField(default="")
    # This is for basic and custom serialisation to return it to client as a JSON.

    def __str__(self):
        return self.link