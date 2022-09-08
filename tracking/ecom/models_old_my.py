from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Product(models.Model):
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Type_pay(models.Model):
    description = models.CharField(max_length=500, null= True)


class Pay(models.Model):

    type_pay  = models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    num_pay = models.CharField(max_length=500,null=True)
    subtotal = models.DecimalField(max_digits = 5, decimal_places = 2)
    send =  models.DecimalField(max_digits = 5, decimal_places = 2)
    total =  models.DecimalField(max_digits = 5, decimal_places = 2)
    

class Orders(models.Model):
    num_order = models.CharField(max_length=500,null=True)
    STATUS =(
        ('Pending Pay','Pending Pay'),
        ('Payment received','Payment received'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    pay = models.ForeignKey('Pay',on_delete=models.CASCADE,null=True)
    product = models.ForeignKey('Orders_list',on_delete=models.CASCADE,null=True)


class Orders_list(models.Model):

    cant = models.BigIntegerField(null=True)
    order=models.ForeignKey('Orders',on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    
    
class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
