from django.db import models
from django.urls import reverse


class News(models.Model):
    #标题
    title = models.CharField(max_length=200)
    #来源
    source = models.CharField(max_length=100)
    #摘要
    digest = models.TextField(blank=True)
    #正文内容
    content = models.TextField()
    #发布时间
    pub_time = models.DateTimeField(auto_now=True)
    #缩略图
    avatar = models.URLField()

    class Meta:
        # 文章按倒序排序
        ordering = ('-pub_time',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[self.id])