from django.contrib import admin
from .models.product import Product
from .models.categories import Categories
from .models.customer import Customer

class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name',]

# class AdminCustomer(admin.ModelAdmin):
#     list_display = ['first_name','last_name','phone_number','email','password']


admin.site.register(Product,AdminProduct)
admin.site.register(Categories,AdminCategory)
admin.site.register(Customer)

# Register your models here.
