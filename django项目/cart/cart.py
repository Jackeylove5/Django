from copy import copy
from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self,request):              # 初始化购物车对象
        # 因为需要session所以需要传入request
        self.session = request.session
        # 操作session存储的字典
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 第一次取不到，向session中存入空白购物车数据
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart =cart



    """
        定义添加商品的方法,接受参数有商品,数量,更新还是修改的判断值
            获取商品id用来作为字典的键所以需要转为字符串
            判断购物车对象内部是否存在此商品如果不存在就生成相应的数据格式对应的数量为0,注意decimal不可以直接进行序列化需要转换为str
            判断如果是更新那么直接将数量进行赋值
            如果是增加那么将数量加等于传入的参数
            调用保存的方法修改session内部数据"""


    def add(self, product, quantity=1, update_quantity=False):
        # 获取商品id，变成json
        product_id = str(product.id)
        # 判断购物车对象内部是否存在此商品，不存在就生成相应的数据格式
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        # 如果是更新直接赋值
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # 设置session.modified的值为True，中间件在看到这个属性的时候，就会保存session
        self.session.modified = True

    def remove(self, product):
        # 从购物车中删除商品
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


# 定义返回数量的方法，返回cart字典的元素对应商品的个数之和
    def __len__(self):
        #购物车内一共有几种商品
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'] * item['quantity']) for item in self.cart.values())

# 定义清空购物车的方法，将session内部对应的购物车的键值对删除
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        # 遍历所有购物车中的商品并从数据库中取得商品对象
        product_ids = self.cart.keys()
        # 获取购物车内的所有商品对象
        products = Product.objects.filter(id__in=product_ids)
        # 复制一份cart字段为了添加单个商品总价的键值对和对应商品对象的键值对
        cart = copy(self.cart)
        # 遍历商品对象，为字典添加保存对象的键值对
        for product in products:
            cart[str(product.id)]['product'] = product
        # 遍历所有的值添加总价并且制作生成器
        for item in cart.values():
            price= Decimal(item.get("price"))
            item['total_price'] = item.get('quantity')*price
            yield item  # 将对象定义成生成器