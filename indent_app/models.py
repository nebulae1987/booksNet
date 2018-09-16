from django.db import models
from index_app.models import Book
from user_app.models import User


# Create your models here.
#地址库表
class Address(models.Model):
    name = models.CharField(max_length=20)
    addr = models.CharField(max_length=200)
    zone = models.CharField(max_length=40)
    zipcode = models.IntegerField()
    telphone = models.IntegerField()
    phone = models.IntegerField()
    user_id = models.ForeignKey(to=User,on_delete=models.CASCADE)
    class Meta:
        db_table = 't_address'

#订单表
class Order(models.Model):
    order_num = models.CharField(max_length=50)
    create_date = models.DateTimeField()
    price = models.FloatField()
    order_addr_id = models.ForeignKey(to=Address,on_delete=models.CASCADE)
    order_user_id = models.ForeignKey(to=User,on_delete=models.CASCADE)
    status = models.SmallIntegerField()
    class Meta:
        db_table = 't_order'

#订单项表：
# class Items(models.Model):
#     book_id = models.ForeignKey(to=Book,on_delete=models.CASCADE)
#     order_id = models.ForeignKey(to=Order,on_delete=models.CASCADE)
#     book_amount = models.IntegerField()
#     total_price = models.FloatField()
#     class Meta:
#         db_table = 't_order_item'

class ItemOrder(models.Model):
    # book_id = models.ForeignKey(to=Book, on_delete=models.CASCADE)
    # order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    book_id = models.IntegerField()
    order_id = models.IntegerField()
    book_amount = models.IntegerField()
    total_price = models.FloatField()
    class Meta:
        db_table = 't_item_order'













