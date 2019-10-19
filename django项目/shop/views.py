from cart.forms import CartAddProductForm
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# 用于列出所有商品，或者根据品类显示某一品类商品
def product_list(request, category_slug=None):
    # None渲染全部商品
    category = None    # 决定列表页显示哪个类别的数据
    # 获取所有的商品类别
    categories = Category.objects.all()    # 决定导航栏显示什么
    # 获取所有的商品
    products = Product.objects.filter(available=True)   # 决定商品栏显示什么
    # 返回列表页进行渲染
    if category_slug:
        # 渲染某一部分商品而非所有的商品
        category = get_object_or_404(categories, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/list.html',
                  {'category': category, 'categories': categories, 'products': products})


def product_detail(request, id, slug):
    # 详情页面视图
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    # 需要修改商品详情页，增加一个add to cart 按钮
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/detail.html',locals())