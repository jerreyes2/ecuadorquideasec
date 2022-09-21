
from django.contrib import admin
from django.urls import path
from ecom import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin', admin.site.urls),
    path('',views.home_view,name=''),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='app/ecom/logout.html'),name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view,name='contactus'),
    path('search', views.search_view,name='search'),
    path('send-feedback', views.send_feedback_view,name='send-feedback'),
    path('view-feedback', views.view_feedback_view,name='view-feedback'),
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='app/ecom/adminlogin.html'),name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),

    path('admin-products', views.admin_products_view,name='admin-products'),
    path('admin-add-product', views.admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),

    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<str:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<str:pk>', views.update_order_view,name='update-order'),
    
    path('delete-detail_order/<int:pk>', views.delete_detail_order,name='delete-detail_order'),
    path('update-detail_order/<int:pk>', views.update_detail_order,name='update-detail_order'),

    path('delete-detail_process/<int:pk>', views.delete_process_tracking,name='delete-detail_process'),
    path('update-detail_process/<int:pk>', views.update_process_tracking,name='update-detail_process'),


    path('customersignup', views.customer_signup_view),
    path('customerlogin', LoginView.as_view(template_name='app/ecom/customerlogin.html'),name='customerlogin'),
    path('customer-home', views.customer_home_view,name='customer-home'),
    path('my-order', views.my_order_view,name='my-order'),
    path('my-order-view/<num_order_>', views.my_order_view_only,name='my_order_view'),
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('edit-profile', views.edit_profile_view,name='edit-profile'),
    path('download-invoice/<num_order>', views.download_invoice_view,name='download-invoice'),
    path('detail_order/<num_order_>', views.detail_order_,name='detail_order'),
    path('add_process_tracking/<num_order_>', views.add_process_tracking,name='add_process_tracking'),

    path('add-to-cart/<int:pk>', views.add_to_cart_view,name='add-to-cart'),
    path('cart', views.cart_view,name='cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view,name='remove-from-cart'),
    path('customer-address', views.customer_address_view,name='customer-address'),
    path('payment-success', views.payment_success_view,name='payment-success'),

    path('add_detail_order', views.add_detail_order,name='add_detail_order'),
    path('tracking', views.tracking,name='tracking'),
    path('tracking_search', views.tracking_search,name='tracking_search'),

    path('events', views.events,name='events')
   

]
