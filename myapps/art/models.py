from django.db import models
from DjangoUeditor.models import UEditorField  # 富文本编辑的字段类型


# Create your models here.
class Tag(models.Model):  # 分类模型类
    name = models.CharField(max_length=50,
                            verbose_name='分类名称',
                            unique=True)

    add_time = models.DateTimeField(auto_now_add=True,
                                    verbose_name='添加时间')

    def __str__(self):  # 避免admin后台显示 object
        return self.name

    class Meta:
        db_table = 't_tag'
        ordering = ['-add_time']
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name  # 去掉s 复数字母


class Art(models.Model):  # 文章的模型类
    title = models.CharField(max_length=100,
                             verbose_name='标题')
    author = models.CharField(max_length=50,
                              verbose_name='作者')

    state = models.IntegerField(choices=((0, '连载中'), (1, '已完本')),
                                verbose_name='状态', default=0)

    summary = models.CharField(max_length=200,
                               verbose_name='简介')

    # content 文章内容 ，也可以文章章节类
    # content = models.TextField(verbose_name='正文')
    content = UEditorField(verbose_name='正文',
                           width=800, height=600,  # 富文本前端组件的大小
                           imagePath='ueditor/images',  # 内容添加的图片保存的位置
                           filePath='ueditor/files',    # 附件中上传文件的位置
                           toolbars='full',
                           blank=True)

    publish_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name='发布时间')

    last_refresh_date = models.DateTimeField(auto_now=True,
                                             verbose_name='更新时间')

    tag = models.ForeignKey(Tag,
                            verbose_name='分类',
                            on_delete=models.SET_NULL,
                            null=True)

    cover = models.ImageField(verbose_name='封面',
                              upload_to='art/images',
                              null=True,
                              blank=True)  # 相当于MEDIA_ROOT

    @property
    def stateName(self):
        return '已完本' if self.state else '连载中'

    def __str__(self):
        return self.title

    class Meta:
        db_table = 't_art'
        verbose_name = '文章'
        verbose_name_plural = verbose_name