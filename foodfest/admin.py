from django.contrib import admin

# Register your models here.
from . models import Product, OrderPost, PersonDetails, PaymentDetail,Profile

admin.site.register(Product)
admin.site.register(OrderPost)
admin.site.register(PersonDetails)
admin.site.register(PaymentDetail)
admin.site.register(Profile)