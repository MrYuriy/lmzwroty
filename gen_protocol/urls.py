from os import name
from django.urls import path
from . import views
import gen_protocol
from django.contrib import admin
urlpatterns = [
    path('', views.home, name='home'),
    #path('', views.fun1, name='home'),
    path('order-form', views.oredr_form, name='order_form'),
    path('new-order', views.new_order, name='new_order'),
    path('ajax/get-response', views.show_name, name='get_response'),
    path('ajax/saveorder', views.saveorder, name='saveorder'),
    path('ajax/add-product-to-order', views.add_product_to_order, name='add_product_to_order'),
    path('save-sku', views.write_sku_to_db),
    path('sow-detail-order', views.show_detail_order),
    path('generate-order-pdf', views.generate_protocol_lm, name='generate_order_pdf'),
    path('generate-pdf-lm', views.generate_pdf_lm, name='generate_pdf_lm'),
    path('generate-pdf-order-todey', views.generate_protocol_products_order_today, name='generate_pdf_order_todey'),
    path('generate-pdf-returned-products', views.generate_pdf_returned_products, name='generate_pdf_returned_products'),
    path('gswrite',views.gswrite, name='gswrite'),
   
]