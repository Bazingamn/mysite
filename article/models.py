from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image


class ArticleColumn(models.Model):
    #栏目标题
    title = models.CharField(max_length=100, blank=True)
    #创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。
    # 多个ArticlePost对象关联至一个User对象
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created_time = models.DateTimeField(default=timezone.now)

    # 文章更新时间，指定每次数据更新时自动写入当前时间
    updated_time = models.DateTimeField(auto_now=True)

    #存储正整数
    total_views = models.PositiveIntegerField(default=0)

    # 标签采用多对多，即一篇文章可以有多个标签，一个标签下也有多篇文章
    tags = TaggableManager(blank=True)

    #文章栏目的一对多外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)
        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 200
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        ordering = ('-created_time',)   #文章按倒序排序

    def __str__(self):
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])


