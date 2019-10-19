from django.shortcuts import render

# Create your views here.
from cart.cart import Cart
from orders.form import OrderCreateForm
from orders.models import OrderItem

"""
创建订单的视图函数order_create
通过Cart类生成cart对象
判断请求方式
    如果是POST请求那么就进行表单校验
        校验通过
            调用表单的save()方法生成一条记录
            遍历购物车对象
            创建订单详情信息
        清空购物车信息
        渲染创建的页面
    如果不是POST请求
        生成表单对象
        渲染创建页面"""
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
    if form.is_valid():
        order = form.save()
        for item in cart:
            # item --> 数量,总价格,商品对象,单价
            # 给此订单去商品详情表内部创建记录
            OrderItem.objects.create(order=order,product=item['product'],
                                     price=item['price'],quantity=item['quantity'])
        cart.clear()
        return render(request,'order/created.html',{'order':order})
    else:
        form = OrderCreateForm()
        return render(request,'order/create.html',locals())

