from index_app.models import Book

#购物车物品项：
class CartItem:
    def __init__(self,book,amount):
        self.book = book
        self.amount = amount
#购物车：
class Cart:
    def __init__(self):
        self.carItem = []
        self.total_price = 0
        self.save_price = 0
    #计算购物车商品总价和节省总价
    def sumPrice(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.carItem:
            self.total_price += i.book.dprice*i.amount
            self.save_price += (i.book.price - i.book.dprice) * i.amount
    #通过图书id，把图书对象添加到购物车对象中
    def addCart(self,bookid,book_amount=1):
        for i in self.carItem:
            #如果购物车中已经有该书，添加数量即可
            if i.book.id == bookid:
                i.amount += book_amount
                print('i.book.amount:',i.amount)
                self.sumPrice()
                return None
        #购物车没有该书则创建购物车项
        book = Book.objects.get(pk = bookid)
        mybook = CartItem(book,book_amount)
        self.carItem.append(mybook)
        self.sumPrice()
    #删除购物车商品
    def delCart(self,bookid):
        for i in self.carItem:
            #如果购物车中已经有该书，去掉所有
            if i.book.id == bookid:
                print('del server ing:',i.book.id)
                self.carItem.remove(i)
                self.sumPrice()
                return None

    #修改购物车商品数量
    def changeCart(self,bookid,book_amount):
        for i in self.carItem:
            #修改购物车商品为用户提交的数量
            if i.book.id == bookid:
                i.amount = book_amount
                print('i.book.amount:',i.amount)
                self.sumPrice()
                return None