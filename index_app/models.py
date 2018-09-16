from django.db import models


#图书分类
class Category(models.Model):
    category_name = models.CharField(max_length=20)
    book_counts = models.IntegerField()
    category_p = models.IntegerField()
    class Meta:
        db_table = 't_category'

#书籍
class Book(models.Model):
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=20)
    pub_company = models.CharField(max_length=50)
    pub_time = models.DateField()
    revision = models.IntegerField()
    ISBN = models.CharField(max_length=64)
    word_count = models.IntegerField()
    page_count = models.IntegerField()
    page_type = models.CharField(max_length=64)
    paper = models.CharField(max_length=64)
    wrapper = models.CharField(max_length=64)
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE)
    price = models.FloatField()
    dprice = models.FloatField()
    editor_recommend = models.CharField(max_length=2000)
    digest_img = models.ImageField(upload_to='book_digest_pic')
    book_img  = models.ImageField(upload_to='book_pic')
    print_time  = models.DateField()
    impression = models.CharField(max_length=64)
    stock = models.IntegerField()
    online_date = models.DateField()
    score = models.IntegerField()
    sales = models.IntegerField()
    class Meta:
        db_table = 't_book'

