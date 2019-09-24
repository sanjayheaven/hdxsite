from django.db import models
from django.contrib.auth.models import User


from simditor.fields import RichTextField
'''
verbose_name=None, name=None, primary_key=False,
        max_length=None, unique=False, blank=False, null=False,
        db_index=False, rel=None, default=NOT_PROVIDED, editable=True,
        serialize=True, unique_for_date=None, unique_for_month=None,
        unique_for_year=None, choices=None, help_text='', db_column=None,
        db_tablespace=None, auto_created=False, validators=(),
        error_messages=None
'''
'''
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True ###just change the str 'TRUE/FALSE' to the slogan
    was_published_recently.short_description = 'Published recently?'
'''
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="名称")
    owner = models.ForeignKey(User, verbose_name="作者",on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    owner = models.ForeignKey(User, verbose_name="作者",on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS_NORMAL = 0
    STATUS_DELETE = 1
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    status = models.PositiveIntegerField(verbose_name="状态",default=STATUS_NORMAL,choices=STATUS_ITEMS)
    title = models.CharField(max_length=255, verbose_name="标题")
    abstract = models.TextField(max_length=1024, blank=True, verbose_name="摘要")
    content = RichTextField(verbose_name="文章正文")
    category = models.ForeignKey(Category, verbose_name="分类",on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者",on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    total_views = models.PositiveIntegerField(default=0,verbose_name="总访问量")

    def __str__(self):
        return self.title

    def update_total_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views'])

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']