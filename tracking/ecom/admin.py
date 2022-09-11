from django.contrib import admin
from .models import Customer, Detail_Orden, Events, Orden, Orden_list, Pay, Product,Orders,Feedback
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("profile_pic","address","mobile")
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
     list_display = ("name","product_image","price","description","stock")
admin.site.register(Product, ProductAdmin)

#class OrderAdmin(admin.ModelAdmin):
#    pass
#admin.site.register(Orders, OrderAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    pass

admin.site.register(Feedback, FeedbackAdmin)

# Register your models here.


class OrdenAdmin(admin.ModelAdmin):
    list_display = ("num_order","status","order_date","email","address","mobile","subtotal","send","iva","total","customer_id")
    list_filter = (
        ('num_order'),
    )
admin.site.register(Orden, OrdenAdmin)



class DetailOrdenAdmin(admin.ModelAdmin):
    list_display = ("num_order_id", "description","date")
    #search_fields = ['num_order_id']

admin.site.register(Detail_Orden, DetailOrdenAdmin)


class Orden_list_Admin(admin.ModelAdmin):
    pass
admin.site.register(Orden_list, Orden_list_Admin)



class Events_Admin(admin.ModelAdmin):
    list_display = ("tittle","organized","date_start","date_end","time_start","time_end","site","state","contry","description","url")
    list_filter = (
        ('id'),
    )
admin.site.register(Events, Events_Admin)


class PayAdmin(admin.ModelAdmin):
    list_display = ("num_pay","num_order","type_pay","total_pay","status","deposit_imag","num_depos")
    list_filter = (
        ('num_pay'),
    )


admin.site.register(Pay , PayAdmin )


"""
class Orders_listAdmin(admin.ModelAdmin):
    pass

admin.site.register(Orders_list , Orders_listAdmin )



class Type_payAdmin(admin.ModelAdmin):
    pass

admin.site.register(Type_pay, Type_payAdmin)

class Orders_listAdmin(admin.ModelAdmin):
    pass

admin.site.register(Orders_list , Orders_listAdmin )

class PayAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pay , PayAdmin )

"""