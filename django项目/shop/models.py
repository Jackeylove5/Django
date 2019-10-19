from django.db import models
from django.urls import reverse

# Create your models here.
# 商品类别表
class Category(models.Model):
    # 类别名称，url所用的字段
    name=models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)           # 商品简称，用于创建规范化URL

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
# 获取详情页
    def get_absolute_url(self):
        # product_list_by_category 路由里的name
        return reverse('shop:product_list_by_category', args=[self.slug])


# 商品详情
class Product(models.Model):
    # 多对一关系，关联到Category模型的外键
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)   #  类别  级联删除
    name = models.CharField(max_length=200, db_index=True)   # 做成索引查询效率高，插入效率低
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)  # 图片所放位置
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)   # 是否上架
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'commodity'
        verbose_name_plural = verbose_name
        index_together = (('id', 'slug'),)    # 联合索引

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # get_absolute_url()是很好的获取具体对象规范化URL的方法。
        return reverse('shop:product_detail', args=[self.id, self.slug])
