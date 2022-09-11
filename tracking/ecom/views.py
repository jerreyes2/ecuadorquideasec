from concurrent.futures import process
from itertools import product
from pyexpat import model
import string
from traceback import print_tb
from urllib import request, response
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
import datetime
import re

def home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    
    cant_prod= models.Product.objects.count()

    return render(request,'app/ecom/index.html',{'cant_prod':cant_prod, 'products':products,'product_count_in_cart':product_count_in_cart})

#def home_view(request):
#    return render(request,'app/ecom/index.html')
    
    #return render(request,'ecommerce/customer_navbar.html')
#for showing login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def customer_signup_view(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}

    if request.method=='POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST,request.FILES)

        if userForm.is_valid() and customerForm.is_valid():
           
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
            messages.success(request, 'Successfully registered user! login.')

        return HttpResponseRedirect('customerlogin')
    return render(request,'app/ecom/customersignup.html',context=mydict)

#-----------for checking user iscustomer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()



#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CUSTOMER
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('admin-dashboard')

#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):

    """
    # for cards on dashboard
    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    # for recent order tables
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'app/ecom/admin_dashboard.html',context=mydict)
    """
    # for cards on dashboard

    orders_ = models.Orden.objects.all()
    customer = models.Customer.objects.all()
    user = models.User.objects.all()


    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orden.objects.all().count()

    # for recent order tables
    orders=models.Orden.objects.all()
    #orders_list = models.Orders_list.objects.all()

    

    mydict={
        'customercount':customercount,
        'productcount':productcount,
        'ordercount':ordercount,
        "orders_":orders_,
        "customer": customer,
        "user": user
    }


    return render(request,'app/ecom/admin_dashboard.html',context=mydict )


# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'app/ecom/view_customer.html',{'customers':customers})

# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'app/ecom/admin_update_customer.html',context=mydict)

# admin view the product
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'app/ecom/admin_products.html',{'products':products})


# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'app/ecom/admin_add_products.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'app/ecom/admin_update_product.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):

    orders_ = models.Orden.objects.all()
    customer = models.Customer.objects.all()
    user = models.User.objects.all()

    mydict={
          
            "orders_":orders_,
            "customer": customer,
            "user": user
        }


    return render(request,'app/ecom/admin_view_booking.html',context=mydict )

    """orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'app/ecom/admin_view_booking.html',{'data':zip(ordered_products,ordered_bys,orders)})"""


@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.Orden.objects.get(num_order=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=models.Orden.objects.get(num_order=pk)
    orderForm=forms.OrderForm(instance=order)
    pay = models.Pay.objects.get(num_order=pk)
    
    status = "Confirmed"
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            ord_stat = order.status
            print("estado...."+str(ord_stat))
            if ord_stat =="Order Confirmed":
                print("sssssssssssssssssssssssssssssi")
                pay = models.Pay.objects.get(num_order=pk)
                pay.status = "Confirmed"
                pay.save()
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'app/ecom/update_order.html',{'orderForm':orderForm,"pay":pay , "status":status})



def add_detail_order(request):

    return render(request,'app/ecom/admin_add_detail_order.html')


@login_required(login_url='adminlogin')
def delete_detail_order(request,pk):
    detail_order=models.Detail_Orden.objects.get(id=pk)
    detail_order.delete()
    return redirect('detail_order/')

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_detail_order(request,pk):
    order=models.Orden.objects.get(num_order=pk)
   
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
           
            orderForm.save()
            return redirect('admin-view-booking')

    return render(request,'app/ecom/update_order.html',{'orderForm':orderForm})


# admin view the feedback
@login_required(login_url='adminlogin')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'app/ecom/view_feedback.html',{'feedbacks':feedbacks})



#---------------------------------------------------------------------------------
#------------------------ PUBLIC CUSTOMER RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'app/ecom/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    
    return render(request,'app/ecom/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})


def tracking(request):

    products=models.Product.objects.all()

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0


    customer = None


    try:
        customer= models.Customer.objects.get(user_id=request.user.id)
    except:
        print("Error....")

    return render(request,'app/ecom/tracking.html', {'products':products,'product_count_in_cart':product_count_in_cart,'customer':customer})



def tracking_search(request):
    # whatever user write in search box we get in query
    
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id = request.user.id)
    num_order_ = request.GET.get('num_order')
    orders = models.Orden.objects.all().filter(num_order = num_order_)
    orden_list = models.Orden_list.objects.all()
    products = models.Product.objects.all()
    detail_order = models.Detail_Orden.objects.all()
    
    #ordered_products = models.Orden_list.objects.all().filter( num_order_id = ordenes)

    #ordered_products=[]

 
    return render(request,'app/ecom/tracking_search.html',{'detail_orders':detail_order,'user':user, 'products': products,'orders' :orders, 'orders_list': orden_list,'product_count_in_cart':product_count_in_cart,'customer':customer})
    
    


    """
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    customer=models.Customer.objects.get(user_id=request.user.id)


    num = request.GET.get('num_order')
   
    orders = models.Orders.objects.all().filter(num_order = num)
 


    if orders != None:
        order_list = models.Orders_list.objects.all().filter(num_order_id = num )


        ordered_products=[]
 

        for order in orders:
                                          #order.product.id
            prod = models.Product.objects.all().filter(id = order.product_id)
            ordered_product= models.Product.objects.all().filter(id = order.product_id)
            ordered_products.append(ordered_product)



    


 
        return render(request,'app/ecom/tracking_search.html',{'data':zip(ordered_products,orders) ,'customer':customer,'orders':orders, 'order_list':order_list , 'prod':prod, 'products':products,'product_count_in_cart':product_count_in_cart,'customer':customer})
    """

# any one can add product to cart, no need of signin
def add_to_cart_view(request,pk):

    products=models.Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    
    cant_prod = models.Product.objects.count()
    customer = None


    try:
        customer= models.Customer.objects.get(user_id=request.user.id)
    except:
        print("Error....")



    response = render(request, 'app/ecom/index.html',{'cant_prod':cant_prod,  'products':products,'customer':customer ,'product_count_in_cart':product_count_in_cart})

   


    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product=models.Product.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')


    return response



# for checkout of cart
def cart_view(request):

    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart=0
    


    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    subtotal = 0
    
    customer = None

    try:
        customer= models.Customer.objects.get(user_id=request.user.id)
    except:
        print("Error....")


    response = None

    if 'product_ids' in request.COOKIES:
        
        product_ids = request.COOKIES['product_ids']

        if product_ids != "":
            product_id_in_cart = product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for p in products:
                subtotal += p.price

            total = (subtotal * 1.12) + 25

            #response.set_cookie('total', total)

            if customer != None:
                response = render(request,'app/ecom/cart.html',{'products':products,'customer':customer ,'subtotal':subtotal,'total':total,'product_count_in_cart':product_count_in_cart})
            else:
                response = render(request,'app/ecom/cart.html',{'products':products,'subtotal':subtotal,'total':total,'product_count_in_cart':product_count_in_cart})

                 
            #total = request.GET.get('total_')
    else:
        response = render(request,'app/ecom/cart.html',{'products':products,'customer':customer ,'subtotal':subtotal,'total':total,'product_count_in_cart':product_count_in_cart})



    return response


## Cantidad de productos
def cart_cant(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products= models.Product.objects.all().filter(id__in = product_id_in_cart)
            #for total price shown in cart
            for p in products:
                total= total + p.price
    return render(request,'app/ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})



def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products = models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for p in products:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'app/ecom/cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response


def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'app/ecom/feedback_sent.html')
    return render(request, 'app/ecom/send_feedback.html', {'feedbackForm':feedbackForm})


#---------------------------------------------------------------------------------
#------------------------ CUSTOMER RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def customer_home_view(request):
   
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
            
    customer=models.Customer.objects.get(user_id=request.user.id)
    
    cant_prod= models.Product.objects.count()


    return render(request,'app/ecom/customer_home.html',{'cant_prod':cant_prod,'products':products,'product_count_in_cart':product_count_in_cart,'customer':customer})






# shipment address before placing order
@login_required(login_url='customerlogin')
def customer_address_view(request):
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address 

   
    total = None

    customer=models.Customer.objects.get(user_id=request.user.id)
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart=True
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0


    subtotal_ = request.GET.get("subtotal_") 
    send_ =  request.GET.get("send_")
    total_ =  request.GET.get("total_")
    iva_ =  request.GET.get("iva_")
    cant_ = None

    if request.method == 'GET':
        global cantidad
        cantidad = request.GET.getlist('tasks[]')
    
        
        print("aaa "+str(cantidad))


        for i in cantidad:
            print("A "+str(i))

    else:
        cant_ = cantidad

    print("valor SUBTOTAL..."+str(subtotal_))
    print("send.. "+str(send_))
    print("valor...TOTAL ... "+str(total_))

    addressForm = forms.AddressForm()
    if request.method == 'POST':
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
           
            # here we are taking address, email, mobile at time of order placement
            # we are not taking it from customer account table because
            # these thing can be changes
            email = addressForm.cleaned_data['Email']
            mobile=addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
            total=0
            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    products=models.Product.objects.all().filter(id__in = product_id_in_cart)
                    for p in products:
                        print
                        #total=total+p.price
                        #total= float(total_)+p.price



            """
            subtotal_ = [float(s) for s in re.findall(r'-?\d+\.?\d*', request.GET.get("subtotal_"))] 
            send_ = [float(s) for s in re.findall(r'-?\d+\.?\d*', request.GET.get("send_"))]
            total_ = [float(s) for s in re.findall(r'-?\d+\.?\d*', request.GET.get("total_"))]
            iva_ = [float(s) for s in re.findall(r'-?\d+\.?\d*', request.GET.get("iva_"))]

            """
           
            products=models.Product.objects.all()
            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                counter=product_ids.split('|')
                product_count_in_cart=len(set(counter))
            else:
                product_count_in_cart=0


            print("Post valor SUBTOTAL..."+str(subtotal_[0]))
            print("Post send.. "+str(send_[0]))
            print("Post valor...TOTAL ... "+str(total_[0]))


            for i in cant_:
                print("Post "+str(i))

            response = render(request, 'app/ecom/payment.html',{'total':total_, 'customer':customer, 'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})
            response.set_cookie('email',email)
            response.set_cookie('mobile',mobile)
            response.set_cookie('address',address)
            response.set_cookie('subtotal', subtotal_)
            response.set_cookie('iva', iva_)
            response.set_cookie('send', send_)
            response.set_cookie('total', total_)
            response.set_cookie('cantidad', cant_)
           
        
        
            #send = 25.00
            #total = float(subtotal * 1.12) + float(send)
            #total= float(total_)+p.price
         
           
            return response
            
    return render(request,'app/ecom/customer_address.html',{'addressForm':addressForm,'customer':customer,'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart, 'subtotal': subtotal_, 'send':send_, 'total':total_, 'iva':iva_})




# here we are just directing to this view...actually we have to check whther payment is successful or not
#then only this view should be accessed

@login_required(login_url='customerlogin')
def payment_success_view(request):
    # Here we will place order | after successful payment
    # we will fetch customer  mobile, address, Email
    # we will fetch product id from cookies then respective details from db
    # then we will create order objects and store in db
    # after that we will delete cookies because after order placed...cart should be empty
  
    customer = models.Customer.objects.get(user_id = request.user.id)
    products= None
    email= None
    mobile= None
    address= None



   
    subtotal = None
    send = None
    total = None
    

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)
            # Here we get products list that will be ordered by one customer at a time

   


    # these things can be change so accessing at the time of order...
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']
    if 'total' in request.COOKIES:
        total=request.COOKIES['total']
    if 'subtotal' in request.COOKIES:
        subtotal=request.COOKIES['subtotal']
    if 'send' in request.COOKIES:
        send=request.COOKIES['send']
    if 'iva' in request.COOKIES:
        iva =request.COOKIES['iva']
    
    

    num_order_ = "EC-"+str(models.Orden.objects.count() + 1)
    num_pay_ = "PY-"+str(models.Pay.objects.count() + 1)
    
    val = ""
    type_pay_ = ""

    #for i in cantidad:
    #    print("pay "+str(i))

    #subtotal = float(total)
    #send = 25.00
    #total = float(subtotal * 1.12) + float(send)

    if request.method == 'POST':
        val = request.POST.get('pay')
        val = "Deposit"
        type_pay_ = val
        num_depos =  request.POST.get('num_depos')
        myfile = request.FILES.get('imagen')

    # here we are placing number of orders as much there is a products
    # suppose if we have 5 items in cart and we place order....so 5 rows will be created in orders table
    # there will be lot of redundant data in orders table...but its become more complicated if we normalize it

  

    models.Orden.objects.get_or_create( num_order = num_order_, status='Pending', email=email,address=address, mobile=mobile, iva = iva ,subtotal= subtotal, send=send, total=total, customer=customer)

    orden = models.Orden.objects.get(num_order = num_order_)

    for product, cant in zip (products , cantidad) :
       # models.Orders.objects.get_or_create(customer=customer, num_order = num_order_, product = product,status='Pending',email=email,mobile=mobile,address=address, cant= cant)
        
        models.Orden_list.objects.get_or_create( cant= cant, num_order = orden , product = product )


    #models.Orders_list.objects.get_or_create( subtotal= subtotal, send=send, total=total, num_order = num_order_ )
    models.Pay.objects.get_or_create( num_pay = num_pay_, num_order = num_order_, total_pay = total, status='Pending', type_pay = type_pay_ , deposit_imag = myfile, num_depos = num_depos)

    num_order_ = 0

  

    # after order placed cookies should be deleted
    response = render(request,'app/ecom/payment_success.html',{'customer':customer,'product_count_in_cart': 0})
    response.delete_cookie('product_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    response.delete_cookie('total')
    response.delete_cookie('subtotal')
    response.delete_cookie('send')
    response.delete_cookie('iva')
    response.delete_cookie('cantidad')
    return response





def events(request):

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0


    events = models.Events.objects.all()


    customer = None

    try:
        customer= models.Customer.objects.get(user_id=request.user.id)
    except:
        print("Error....")
    #return render(request,'app/ecom/events.html',{'user':user,'orders' :orders,'product_count_in_cart':product_count_in_cart,'customer':customer})
    
    return render(request,'app/ecom/events.html',{'product_count_in_cart':product_count_in_cart,'customer':customer, 'events':events})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_order_view(request):

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0


    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id = request.user.id)
    orders = models.Orden.objects.all().filter(customer_id = customer)

    return render(request,'app/ecom/my_orders.html',{'user':user,'orders' :orders,'product_count_in_cart':product_count_in_cart,'customer':customer})

    # Funcional
    """
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    customer = models.Customer.objects.get(user_id=request.user.id)
    orders = models.Orden.objects.all().filter(customer_id = customer)
    orden_list = models.Orden_list.objects.all()
    products = models.Product.objects.all()
    user = models.User.objects.get(id = request.user.id)
  
 
    return render(request,'app/ecom/my_orders.html',{'user':user,'products': products,'orders' :orders, 'orders_list': orden_list,'product_count_in_cart':product_count_in_cart,'customer':customer})
    """



def detail_order_(request, num_order_):

    detail_orders = models.Detail_Orden.objects.all().filter(num_order_id = num_order_)

    global num__order_ 
    num__order_= num_order_
    
    return render(request,'app/ecom/admin_detail_order.html',{"detail_orders":detail_orders, "num_order":num_order_})


num__order_ = ""


def add_process_tracking(request, num_order_):


    global num__order_ 
    num__order_= num_order_

    
    if request.method == "POST":
        date =  request.POST["date"]
        description =  request.POST["description"]

        try:
            procces = models.Detail_Orden.objects.create(date = date , description= description, num_order_id = num__order_)
            messages.success(request, '¡Save Success !')
            print("todo excelente")

            detail_orders = models.Detail_Orden.objects.all().filter(num_order_id = num_order_)

            return render(request,'app/ecom/admin_detail_order.html',{"detail_orders":detail_orders, "num_order":num_order_})
        except:
            print("Error!! Contact system technical support..")

        print("post...")
        
    
    if request.method == "GET":
        print("get...")

    return render(request,'app/ecom/admin_add_detail_order.html',{"num_order":num_order_})



def delete_process_tracking(request, pk):



    try:
        process = models.Detail_Orden.objects.get(id=pk)
        process.delete()
        messages.success(request, '¡Delete Success !')
        print("todo excelente")
    except:
        print()


    detail_orders = models.Detail_Orden.objects.all().filter(num_order_id = num__order_)
    return render(request,'app/ecom/admin_detail_order.html',{"detail_orders":detail_orders})

   


def update_process_tracking(request, pk):

    if request.method == "POST":

        
        try:
            
            date =  request.POST["date"]
            description =  request.POST["description"]

            process = models.Detail_Orden.objects.get(id=pk)

            process.date = date
            process.description = description
            process.save()
            
            messages.success(request, '¡Update Success !')
            print("todo excelente actualizado")

           
        except:
            print()

        print("post...")

    
        detail_orders = models.Detail_Orden.objects.all().filter(num_order_id = num__order_)
        return render(request,'app/ecom/admin_detail_order.html',{"detail_orders":detail_orders})


    
    if request.method == "GET":
        process = models.Detail_Orden.objects.get(id=pk)


        return render(request,'app/ecom/admin_update_detail_order.html',{"process":process})
        



def my_order_view_only(request, num_order_):
    # whatever user write in search box we get in query
    
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    customer = models.Customer.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id = request.user.id)
    orders = models.Orden.objects.all().filter(num_order = num_order_)
    orden_list = models.Orden_list.objects.all()
    products = models.Product.objects.all()
    detail_order = models.Detail_Orden.objects.all()
    
    #ordered_products = models.Orden_list.objects.all().filter( num_order_id = ordenes)

    #ordered_products=[]

 
    return render(request,'app/ecom/tracking_search.html',{'detail_orders':detail_order,'user':user, 'products': products,'orders' :orders, 'orders_list': orden_list,'product_count_in_cart':product_count_in_cart,'customer':customer})
    
#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def download_invoice_view(request,orderID,productID):
    order=models.Orders.objects.get(id=orderID)
    product=models.Product.objects.get(id=productID)
    mydict={
        'orderDate':order.order_date,
        'customerName':request.user,
        'customerEmail':order.email,
        'customerMobile':order.mobile,
        'shipmentAddress':order.address,
        'orderStatus':order.status,

        'productName':product.name,
        'productImage':product.product_image,
        'productPrice':product.price,
        'productDescription':product.description,
    }
    return render_to_pdf('app/ecom/download_invoice.html',mydict)






@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def my_profile_view(request):

    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'app/ecom/my_profile.html',{'customer':customer, 'products':products,'product_count_in_cart':product_count_in_cart})


@login_required(login_url='customerlogin')
@user_passes_test(is_customer)
def edit_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
    return render(request,'app/ecom/edit_profile.html',context=mydict)



#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START --------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'app/ecom/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'app/ecom/contactussuccess.html')
    return render(request, 'app/ecom/contactus.html', {'form':sub})
