from django.contrib import admin
from gen_protocol.models import Product , Order, OrderProduct, SkuName
admin.site.register(Product)
#admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(SkuName)

class OrderedProductInline(admin.TabularInline):
    exclude = []
    model = OrderProduct
    classes = ['collapse']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderedProductInline,
    ]