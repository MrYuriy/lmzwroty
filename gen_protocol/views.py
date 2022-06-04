
from django.shortcuts import render
from django.http import JsonResponse, request, FileResponse
from reportlab.pdfbase.pdfdoc import count
from .models import Order, Product, OrderProduct, SkuName
from django.http import HttpResponse

import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
#from mongoengine import *

from datetime import date, datetime
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import os
#import parser 
#from .parser import get_name_sku_from_website_LM
import pymongo

import requests
from bs4 import BeautifulSoup

def get_name_sku_from_website_LM(sku):
    
    link = f"https://www.leroymerlin.pl/szukaj.html?q={sku}&sprawdz=true"
    name_of_product_and_sku =get_name_sku_of_product(link)
    
    return(name_of_product_and_sku)

def get_soup(url):
    
    r = requests.get(url )
    
    if r == None:
        return None
    else:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup



def get_name_sku_of_product(url):
    soup = get_soup(url)

    name_of_product = soup.find('div', class_="product-description").find('div',class_="product-title" ).find('h1').string
    sku = int(soup.find('div', class_="product-description").find('div', class_="ref-number").find('span').string)
    resolt = {"name_of_product":name_of_product, "sku":sku}
    #print (resolt) 
    return(resolt)


def return_name_of_product (sku_r):
    try:
        
        name_of_product = SkuName.objects.filter(sku = int(sku_r)).last().name_of_produckt
        
        #print(SkuName.objects.filter(sku = int ))
        #name_of_product = get_name_sku_from_website_LM(int(sku_r))[name_of_product]
        if (len(name_of_product)<=24):
            return name_of_product
        if name_of_product[24]!=" ":
            name_of_product = name_of_product[:24]
            
            name_of_product = name_of_product.split(' ')
            name_of_product = name_of_product[:-1]
            name_of_product = ' '.join(map(str, name_of_product))
        else:
            name_of_product = name_of_product[:24]
        return name_of_product
    except:
        try :
            name_of_product= get_name_sku_from_website_LM(sku_r)['name_of_product']
            sku_r = get_name_sku_from_website_LM(sku_r)['sku']
           
            product = SkuName(sku=sku_r, name_of_produckt = name_of_product)
            product.save()
           
            
        # except : 
        #     name_of_product= get_name_sku_from_website_LM(sku_r)['name_of_product']
        #     print(sku_r)
        #     #print(name_of_product)
        #     product = SkuName(sku=sku_r, name_of_produckt = name_of_product)
        #     product.save()
        #     print (product)
        except:
            name_of_product = "name not found"
        return name_of_product


 

def home(request):
    return render(request, 'gen_protocol/home.html')

def oredr_form(request):
    nrorder = request.GET.get('nrorder')
    return render(request, 'gen_protocol/order_form.html', {"nrorder":nrorder})

def new_order(request):
    nr_order = request.GET.get('nrorder')
    return render(request, 'gen_protocol/new_order.html', {"nrorder":nr_order})


def show_name(request):
    user_input = request.GET.get('sku')
    name_of_product = return_name_of_product(user_input)
    # print(name_of_product)
    data = {'response': f'Name of product: {name_of_product}',}
    return JsonResponse(data)

def saveorder(request):
    nrorder = request.GET.get('nrorder')
    tapeofdelivery = request.GET.get('tapydelivery')
    if (nrorder!='' and tapeofdelivery!=''  ):
        order = Order( nr_order=int(nrorder), tape_of_delivery = tapeofdelivery, date_writes=date.today())
        order.save()




    # print(order)
    return HttpResponse(status = 200)

def add_product_to_order(request):
    nrorder = request.GET.get('nrorder')
    sku_product = get_name_sku_from_website_LM(int(request.GET.get('sku')))['sku']
    quantity = int(request.GET.get('quantity'))
    quantity_not_damaget = int(request.GET.get('quantity_not_damaget'))
    q_damage_products = int(quantity)-int(quantity_not_damaget)
    if ( sku_product=='' or quantity==''or quantity_not_damaget=='' ):
        return HttpResponse(status = 200)

    name_of_product = return_name_of_product(sku_product)

    order = Order.objects.filter(nr_order=nrorder).last()
    id_order = order.id
    #
    if OrderProduct.objects.filter(order_id=id_order,product__sku=sku_product ):
        order_product = OrderProduct.objects.get(order_id=id_order,product__sku=sku_product )
        new_product = order_product.product

        new_product.quantity += quantity
        new_product.quantity_not_damaget +=quantity_not_damaget
        new_product.quantity_damage += q_damage_products

        new_product.save()
        order_product.product = new_product
        order_product.save()

    else:
        new_product = Product(name = name_of_product,sku=sku_product, quantity=quantity, quantity_not_damaget=quantity_not_damaget , quantity_damage=q_damage_products)
        new_product.save()
        order_product = OrderProduct(order=order, product=new_product)
        order_product.save()
    
    return HttpResponse(status = 200)


def write_sku_to_db(reqest):
    i = 0
    file = open('sku_name_of_product1.txt', 'r', encoding="utf-8")
    for line in file:
        line = line.replace('\n','')
        sku = int(line.split(':')[0].replace("'",'').replace('{',''))
        name_of_product = line.split("'")[1].replace("'",'').replace('}','')
        product = SkuName(sku=sku, name_of_produckt = name_of_product)
        
        product.save()
        #print(product)
    return HttpResponse("Hello, world. You're at the polls index.")

def show_detail_order(request):#доробити як буде скучно !!!!!!!!!!!
    #nrorder = request.GET.get('nrorder')
    nrorder = 554443
    order = Order.objects.get(nr_order=nrorder)
    id_order = order.id
    #orderproduct =  OrderProduct.objects.all()
    orderproduct = OrderProduct.objects.filter(order_id=id_order)
    products = []
    for product in orderproduct:
        name=(product.product.sku)
        products.append(name)
    return HttpResponse(products)

def get_order_detail(o_id):
    #order = Order.objects.filter(nr_order = nrorder).last()
    id_order = o_id
    order = Order.objects.get(id = o_id)
    tape_of_delivery = order.tape_of_delivery
    date_writes = order.date_writes
    orderproducs = OrderProduct.objects.filter(order_id = id_order)
    date_to_print_order = {'not_damage':None,'damage':None,'tape_of_delivery':None}
    sku_quantity_damage = []
    sku_quantity_not_damage = []
    # sku_s = []
    # damage_product = []
    # not_damage_product = []
    for product in orderproducs:
        if product.product.quantity_not_damaget:
            value_sku = product.product.sku
            value_not_damage_product = product.product.quantity_not_damaget
            sku_quantity_not_damage.append([value_sku,value_not_damage_product])

        if product.product.quantity_damage:
            value_sku = product.product.sku
            value_damage_product = product.product.quantity_damage
            sku_quantity_damage.append([value_sku,value_damage_product])
  
    date_to_print_order['not_damage']=sku_quantity_not_damage
    date_to_print_order['damage']=sku_quantity_damage
    date_to_print_order['tape_of_delivery']=str(tape_of_delivery)
    date_to_print_order['nr_order']=order.nr_order
    date_to_print_order['date_writes']=date_writes
    #print("ok")
    return (date_to_print_order)


def generate_pdf_lm(request):
    #print("okkkk")
    nrorder = request.GET.get('nrorder')
    order = Order.objects.filter(nr_order=nrorder).last()
    orderdetail = get_order_detail(order.id)
    list_not_damage_product = orderdetail['not_damage']
    list_damage_product = orderdetail['damage']
    buffer = io.BytesIO()
    my_canvas = canvas.Canvas(buffer)
    step=0
    for i in range((max(len(list_damage_product),len(list_not_damage_product))//15)+1):
        my_canvas.drawImage('static/img/protocol_lm.jpg' ,-30, -100, width=652, height=960)
        my_canvas.setFont('Helvetica', 16)#розмір шрифту і вид шрифту
        step += 15
        Y = 729 #початкова точка по Y для цілих
        if list_not_damage_product[step-15:step]:
            for sku_val in list_not_damage_product[step-15:step]:
                my_canvas.drawString(235, Y, str(sku_val[0]))# координати потім текст
                my_canvas.drawString(500, Y, str(sku_val[1]))
                Y-=22#Крок між рядками
        Y = 355 #точка початку по Y для пощкоджених
        if list_damage_product[step-15:step]:
            for sku in list_damage_product[step-15:step]:
                my_canvas.drawString(235, Y, str(sku[0]))# координати потім текст
                my_canvas.drawString(500, Y, str(sku[1]))
                Y-=22#Крок між рядками
        my_canvas.showPage()
    my_canvas.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=False, filename="Zwrot_LM.pdf")

def generate_protocol_lm(request):
    return render(request,'gen_protocol/print_protokol_to_lm.html')

def generate_protocol_products_order_today(request):
    return render(request,'gen_protocol/print_protokol_returned_products.html',{"data_today":date.today().strftime("%Y-%m-%d")})
 
 
def generate_pdf_returned_products(request):
    buffer = io.BytesIO()
    date_to_print = request.GET.get("date_to_print").replace('-','/').split('/')
    date_to_print = str(date_to_print[2]+'/'+date_to_print[1]+'/'+date_to_print[0])
    date_to_print = datetime.strptime(date_to_print,'%d/%m/%Y')
    pdfmetrics.registerFont(TTFont('FreeSans', 'freesans/FreeSans.ttf'))
    my_canvas = canvas.Canvas(buffer)
    my_canvas.drawImage('static/img/returned_products_order.jpg' ,-10, 0, width=622, height=850)
    my_canvas.setFont('FreeSans', 12)#розмір шрифту і вид шрифту   
    list_order_today = Order.objects.filter(date_writes = date_to_print)#date.today() dont foget set tis pharamether
    #list_order_today = Order.objects.all()
    Y=610
    counter = 0
    for order in list_order_today:
        nrorder = order.nr_order
        #print(nrorder)
        if counter==21:
                    my_canvas.showPage()
                    my_canvas.setFont('FreeSans', 12)
                    my_canvas.drawImage('static/img/returned_products_order.jpg' ,-10, 0, width=622, height=850)
                    Y=610
                    counter=0
        all_about_order=get_order_detail(order.id)
        my_canvas.drawString(440,Y,str(all_about_order['tape_of_delivery']))
        #my_canvas.drawString(500,Y,str(nrorder))
        if str(nrorder) == "0":
            my_canvas.drawString(495,Y,"Brak nr.zam.")
        else:
            my_canvas.drawString(500,Y,str(nrorder))

        for dicts in [[all_about_order['not_damage'],'P'],[all_about_order['damage'],'U']]:
            
            for product in dicts[0]:
                if counter==21:
                    my_canvas.showPage()
                    my_canvas.setFont('FreeSans', 12)
                    my_canvas.drawImage('static/img/returned_products_order.jpg' ,-10, 0, width=622, height=850)
                    Y=610
                    counter=0
                my_canvas.drawString(55,Y,str(product[0]))
                name_of_product = str(return_name_of_product(product[0]))[:25]
                my_canvas.drawString(131,Y, name_of_product )
                my_canvas.drawString(310,Y,str(product[1]))
                my_canvas.drawString(380,Y,str(dicts[1]))
                counter +=1
                Y-=21
                
    my_canvas.showPage()
    my_canvas.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=False, filename="Zwrotu_od_klientow.pdf")


def gen_value_for_gsheet(nr_order_list):
    values=[]
    not_damage_list = []
    damage_list = []
    for order in nr_order_list:

        products_list_not_damage = get_order_detail(int(order.id))['not_damage']
        products_list_damage = get_order_detail(int(order.id))['damage']
        # print(str(get_order_detail(int(order.nr_order))['date_writes']))
        # print(str(get_order_detail(int(order.nr_order))['date_writes'].strftime("%d.%m.%Y")))
        date_writes = str(get_order_detail(int(order.id))['date_writes'].strftime("%d.%m.%Y"))
        #print('product list- :',products_list_not_damage)
        for sku in products_list_not_damage:
            list_row = []
            list_row.append(date_writes)
            list_row.append(sku[0])
            list_row.append(return_name_of_product(sku[0]))
            list_row.append(sku[1])#кількість продукту
            list_row.append('')
            list_row.append('')
            list_row.append(int(order.nr_order))
            list_row.append('')
            list_row.append('')
            #print('list row-: ',list_row)
            not_damage_list.append(list_row)
        values.append(not_damage_list)

        for sku in products_list_damage:
            list_row = []
            list_row = []
            list_row.append(date_writes)
            list_row.append(sku[0])
            list_row.append(return_name_of_product(sku[0]))
            list_row.append(sku[1])#кількість продукту
            list_row.append('')
            list_row.append('')
            list_row.append(int(order.nr_order))
            list_row.append('')
            list_row.append('')
            damage_list.append(list_row)
        values.append(damage_list)
    # print(values)
    return values

def gswrite(request):
    CREDENTIALS_FILE = 'zwrotylm_sekret.json'
    # ID Google Sheets документа (можно взять из его URL)
    spreadsheet_id = '1ctyFK5xqUz40R5Kx0ksPYJ0bEqmMz4sVGbXFey9LfgA'

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    
    result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range="P!A1:E").execute()
    rows = result.get('values', [])
    coordinateP=int((len(rows)))+1

    result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id, range="U!A1:E").execute()
    rows = result.get('values', [])
    coordinateU=int((len(rows)))+1

    #datetime_object = datetime.strptime('2022-01-09', "%Y-%m-%d").date()
    list_order_today = Order.objects.filter(date_writes= date.today())#виклик функції для генерації запису в google sheets
    print(list_order_today)
    values = gen_value_for_gsheet(list_order_today)
    #values = gen_value_for_gsheet([555,999])

    value=[
            {"range": "P!A{0}:J".format(coordinateP),
             "majorDimension": "ROWS",
             "values":values[0]},
            {"range": "U!A{0}:J".format(coordinateU),
             "majorDimension": "ROWS",
             "values":values[1]},
            ]


    values = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": value
    }
    ).execute()

    return HttpResponse(status = 200)
#zdfjsfjkla