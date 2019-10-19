from django.db import models
from shop.models import Product
# Create your models here.

class Order(models.Model):
    # 用户姓名,电话,地址,创建时间,更新时间,是够支付,是否发货
    name = models.CharField(max_length=50,verbose_name='姓名')
    tel = models.CharField(max_length=50,verbose_name='电话')
    address = models.CharField(max_length=50,verbose_name='地址')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    send = models.BooleanField(default=False)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class OrderItem(models.Model):
    # 商品的名称 价格 数量
    product = models.ForeignKey(to=Product,to_field='id',on_delete=models.CASCADE,related_name='order_items')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.IntegerField()
    order = models.ForeignKey(to=Order,to_field='id',on_delete=models.CASCADE,related_name='items')

    def __str__(self):
        return 'Order {}'.format(self.order.id)

    def get_cost(self):
        return self.price*self.quantity













