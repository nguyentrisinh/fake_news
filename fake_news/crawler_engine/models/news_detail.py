from django.db import models
from django.utils.html import format_html

from ..constants import NEWS_STATUS


class NewsDetail(models.Model):
    objects = models.Manager()

    # base_url is the domain of the url that we crawl the news
    base_url = models.CharField(max_length=255, null=False, blank=False)
    url = models.CharField(max_length=2048, null=False, blank=False)

    # News detail
    title = models.CharField(max_length=1000, null=True, blank=True)
    top_image_url = models.CharField(max_length=1000, null=True, blank=True)
    # top_image = models.ImageField(upload_to='news/top_images/', null=True, blank=True, max_length=1000)
    details = models.TextField(null=True, blank=True)
    authors = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=1000, null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)

    # status to know the news is real or spam
    status = models.PositiveSmallIntegerField(choices=NEWS_STATUS, default=1)

    # property for management (Don't need to init)
    # time when the news is crawler
    crawled = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return '{}: {}'.format(self.base_url, self.title)

    def colored_title(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            'ff0000',
            self.title,
        )

    def colored_status(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            '00a9ff',
            self.get_status_display()
        )
