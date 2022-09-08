from pyexpat import model
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
    stock = models.BigIntegerField(null=True)
    def __str__(self):
        return self.name


class Orders(models.Model):
    
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    num_order = models.CharField(max_length=500,null=True)
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    cant = models.BigIntegerField(null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)


class Orders_list(models.Model):

    #num_order=models.ForeignKey('Orders',on_delete=models.CASCADE,null=True)
    num_order = models.CharField(max_length=500,null=True)
    subtotal = models.DecimalField(max_digits = 5, decimal_places = 2,null=True)
    send =  models.DecimalField(max_digits = 5, decimal_places = 2,null=True)
    total =  models.DecimalField(max_digits = 5, decimal_places = 2,null=True)



class Pay(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Py Confirmed','Pay Confirmed')
       
    )
    num_pay = models.CharField(max_length=500,null=True)
    num_order = models.CharField(max_length=500,null=True)
    PAY =(
        ('Credit Card','Credit Card'),
        ('PayPal','PayPal')
    )
    type_pay =  models.CharField(max_length=50,null=True,choices=PAY)
    total_pay =  models.DecimalField(max_digits = 5, decimal_places = 2,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)




class Orden(models.Model):
    num_order = models.CharField(max_length=100, primary_key=True)
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    order_date= models.DateField(auto_now_add=True,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    STATE =(
        ('Azuay','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    
    state=models.CharField(max_length=50,null=True,choices= STATE)
    mobile = models.CharField(max_length=20,null=True)
    subtotal = models.DecimalField(max_digits = 5, decimal_places = 2,null=True)
    iva = models.DecimalField(max_digits = 5, decimal_places = 2,null=True)
    send =  models.DecimalField(max_digits = 5, decimal_places = 2,null=True)
    total =  models.DecimalField(max_digits = 5, decimal_places = 2,null=True)



class Orden_list(models.Model):
    num_order = models.ForeignKey('Orden', on_delete=models.CASCADE,null=True)
    product = models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    cant = models.BigIntegerField(null=True)
    


class Detail_Orden(models.Model):
    num_order = models.ForeignKey('Orden', on_delete=models.CASCADE,null=True)
    date= models.DateField(null=True)
    description=models.CharField(max_length=100)
  


class Events(models.Model):
    
    tittle = models.CharField(max_length=200)
    organized = models.CharField(null=True, max_length=100)
    date_start= models.DateField(null=True)
    date_end= models.DateField(null=True)
    time_start = models.TimeField(null=True)
    time_end = models.TimeField(null=True)
    site =  models.CharField(null=True, max_length=100)
    state = models.CharField(null=True, max_length=100)
    contry = models.CharField(null=True, max_length=100)
    description= models.CharField(max_length=200)
    url = models.CharField(null=True, max_length=200)



"""
class Orders_list(models.Model):

    #num_order=models.ForeignKey('Orders',on_delete=models.CASCADE,null=True)
    num_order = models.BigIntegerField(null=True)
    cant = models.BigIntegerField(null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)

"""  
"""   
class Orders(models.Model):
    
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    #product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)
    subtotal = models.DecimalField(max_digits = 5, decimal_places = 2,null=True)
    send =  models.DecimalField(max_digits = 5, decimal_places = 2,null=True)
    total =  models.DecimalField(max_digits = 5, decimal_places = 2,null=True)

"""
class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
