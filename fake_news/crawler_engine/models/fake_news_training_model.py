from django.db import models

from ..constants import NEWS_STATUS


class FakeNewsTrainingModel(models.Model):
    objects = models.Manager()

    # base_url is the domain of the url that we crawl the news
    base_url = models.CharField(max_length=255, null=False, blank=False)
    url = models.CharField(max_length=2048, null=False, blank=False)

    # News detail
    title = models.CharField(max_length=1000, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    # status to know the news is real or fake
    status = models.PositiveSmallIntegerField(choices=NEWS_STATUS, default=1)

    published_date = models.DateTimeField(null=True, blank=True)

    # property for management (Don't need to init)
    # time when the news is crawler
    crawled = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.title
