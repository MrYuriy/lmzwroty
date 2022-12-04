
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
    
    #link = f"https://www.leroymerlin.pl/szukaj.html?q={sku}&sprawdz=true"
    name_of_product_and_sku =get_name_sku_of_product(sku)
    
    
    return(name_of_product_and_sku)
    #eturn(sku)

def get_soup(url):
    

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
    r = requests.get(url, headers=headers)
  
    if r == None:
        return None
    else:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup



def get_name_sku_of_product(sku):
    #url = 'https://retranslator.vercel.app/?sku='+str(sku)
    
    url = f"https://www.leroymerlin.pl/szukaj.html?q={sku}&sprawdz=true"
    soup = get_soup(url)
    
    name_of_product = soup.find('div', class_="product-description").find('div',class_="product-title" ).find('h1').string
    sku = int(soup.find('div', class_="product-description").find('div', class_="ref-number").find('span').string)
    #print("print ok")
    try:
        try:
            imgsrc = soup.find('div',class_='product-gallery').find('div',class_='photo-container').find_all('a')[0].find('img').get('src')
        except:
            imgsrc = soup.find('div',class_='product-gallery').find('div',class_='photo-container').find('img').get('src')
    except:
        imgsrc = ''
    resolt = {"name_of_product":name_of_product, "sku":sku, "imgsrc":imgsrc}
    #print (resolt) 
    return(resolt)


def return_sku_information (sku_r):
    try:
        
        name_of_product = SkuName.objects.filter(sku = int(sku_r)).last().name_of_produckt
        information_of_produckt = get_name_sku_of_product(sku_r)
        #print(SkuName.objects.filter(sku = int ))
        #name_of_product = get_name_sku_from_website_LM(int(sku_r))[name_of_product]
        if (len(name_of_product)<=24):
            imgsrc = information_of_produckt['imgsrc']
            sku_information = {"name_of_product":name_of_product,"imgsrc":imgsrc}
            return sku_information
        if name_of_product[24]!=" ":
            name_of_product = name_of_product[:24]
            
            name_of_product = name_of_product.split(' ')
            name_of_product = name_of_product[:-1]
            name_of_product = ' '.join(map(str, name_of_product))
        else:
            name_of_product = name_of_product[:24]
        imgsrc = information_of_produckt['imgsrc']
        sku_information = {"name_of_product":name_of_product,"imgsrc":imgsrc}
        return sku_information
    except:
        try :
            information_of_produckt=get_name_sku_from_website_LM(sku_r)
            name_of_product= information_of_produckt['name_of_product']
            if (len(name_of_product)>25):
                if name_of_product[24]!=" ":
                    name_of_product = name_of_product[:24]
                    
                    name_of_product = name_of_product.split(' ')
                    name_of_product = name_of_product[:-1]
                    name_of_product = ' '.join(map(str, name_of_product))
                else:
                    name_of_product = name_of_product[:24]
            sku_r = information_of_produckt['sku']
            imgsrc = information_of_produckt['imgsrc']
            print(name_of_product)
            product = SkuName(sku=sku_r, name_of_produckt = name_of_product)
            product.save()

        except:
            imgsrc =''
            name_of_product = "name not found"
    
        sku_information = {"name_of_product":name_of_product,"imgsrc":imgsrc}
        #print(sku_information)
        return sku_information


 

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
    information_to_show = return_sku_information(user_input)
    #print(information_to_show)
    name_of_product = information_to_show['name_of_product']
    src = information_to_show['imgsrc']
    # print(name_of_product)
    data = {'response': f'Name of product: {name_of_product}','imgsrc':src}
    return JsonResponse(data)

def saveorder(request):
    nrorder = request.GET.get('nrorder')
    tapeofdelivery = request.GET.get('tapydelivery')
    if (nrorder!='' and tapeofdelivery!=''  ):
        order = Order( nr_order=int(nrorder), tape_of_delivery = tapeofdelivery, date_writes=date.today())
        order.save()
    return HttpResponse(status = 200)

def add_product_to_order(request):
    nrorder = request.GET.get('nrorder')
    sku_product = get_name_sku_from_website_LM(int(request.GET.get('sku')))['sku']
    quantity = int(request.GET.get('quantity'))
    quantity_not_damaget = int(request.GET.get('quantity_not_damaget'))
    q_damage_products = int(quantity)-int(quantity_not_damaget)
    if ( sku_product=='' or quantity==''or quantity_not_damaget=='' ):
        return HttpResponse(status = 200)
    #print (sku_product)
    name_of_product = return_sku_information(sku_product)['name_of_product']
    #print ('!!!!!!!!!!!!',name_of_product)

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
        #print("ok here !!!!!!!!!!!!!!!!!!!!")
        order_product = OrderProduct(order=order, product=new_product, date_writes=date.today())
        order_product.save()
    #print(order)
    
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

# def get_order_detail(o_id):
def get_order_detail(order, orderproducs):
    #order = Order.objects.filter(nr_order = nrorder).last()
    # id_order = o_id
    # order = Order.objects.get(id = o_id)
    tape_of_delivery = order.tape_of_delivery
    date_writes = order.date_writes
    # orderproducs = OrderProduct.objects.filter(order_id = order.id)
    # orderproducs = 
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
    order_products = OrderProduct.objects.filter(order_id = order.id)
    orderdetail = get_order_detail(order, order_products)
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
    order_products = OrderProduct.objects.filter(date_writes = date_to_print)
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
        all_about_order=get_order_detail(order, order_products.filter(order_id = order.id))
        my_canvas.drawString(440,Y,str(all_about_order['tape_of_delivery']))
        #my_canvas.drawString(500,Y,str(nrorder))
        if str(nrorder) == "0":
            my_canvas.drawString(495,Y,"Brak nr.zam.")
        else:
            my_canvas.drawString(500,Y,str(nrorder))

        for dicts in [[all_about_order['not_damage'],'P'],[all_about_order['damage'],'U']]:
            i = 0
            for product in dicts[0]:
                if counter==21:
                    my_canvas.showPage()
                    my_canvas.setFont('FreeSans', 12)
                    my_canvas.drawImage('static/img/returned_products_order.jpg' ,-10, 0, width=622, height=850)
                    Y=610
                    counter=0
                my_canvas.drawString(55,Y,str(product[0]))
                #name_of_product = str(return_sku_information(product[0])['name_of_product'])[:25]
                #print (order_products.filter(order_id = order.id)[i].product)
                
                name_of_product = (order_products.filter(order_id = order.id)[i]).product.name
                my_canvas.drawString(131,Y, name_of_product )
                my_canvas.drawString(310,Y,str(product[1]))
                my_canvas.drawString(380,Y,str(dicts[1]))
                counter +=1
                Y-=21
                i+=1
                
    my_canvas.showPage()
    my_canvas.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=False, filename="Zwrotu_od_klientow.pdf")

def generate_excel_products_order_today(request):
    return render(request,'gen_protocol/write_excel.html',{"data_today":date.today().strftime("%Y-%m-%d")})
 

def gen_value_for_gsheet(orders, order_products):
    values=[]
    not_damage_list = []
    damage_list = []
    for order in orders:
        all_product_in_order = OrderProduct.objects.filter(order_id = order.id)
        for product in all_product_in_order:
            product = product.product
            if product.quantity_not_damaget:
                list_row = []
                list_row.append((order.date_writes).strftime("%d.%m.%Y"))
                list_row.append(product.sku)
                list_row.append(product.name)
                list_row.append(product.quantity_not_damaget)
                list_row.append('')
                list_row.append('')
                list_row.append(int(order.nr_order))
                list_row.append('')
                list_row.append('')
                not_damage_list.append(list_row)
            if product.quantity_damage:
                list_row = []
                list_row.append((order.date_writes).strftime("%d.%m.%Y"))
                list_row.append(product.sku)
                list_row.append(product.name)
                list_row.append(product.quantity_damage)
                list_row.append('')
                list_row.append('')
                list_row.append(int(order.nr_order))
                list_row.append('')
                list_row.append('')
                damage_list.append(list_row)
    values.append(not_damage_list)
    values.append(damage_list)
    #print(values)
    # for order in orders:
    #     orderproduct = order_products.filter(order_id = order.id)
    #     detail_order = get_order_detail(order, orderproduct)
    #     products_list_not_damage = detail_order['not_damage']
    #     products_list_damage = detail_order['damage']
    #     # products_list_not_damage = get_order_detail(int(order))['not_damage']
    #     # products_list_damage = get_order_detail(int(order))['damage']
    #     # print(str(get_order_detail(int(order.nr_order))['date_writes']))
    #     # print(str(get_order_detail(int(order.nr_order))['date_writes'].strftime("%d.%m.%Y")))
    #     date_writes = detail_order['date_writes'].strftime("%d.%m.%Y")
    #     #print('product list- :',products_list_not_damage)
    #     for sku in products_list_not_damage:
    #         list_row = []
    #         list_row.append(date_writes)
    #         list_row.append(sku[0])
    #         list_row.append(return_sku_information(sku[0])['name_of_product'])
    #         list_row.append(sku[1])#кількість продукту
    #         list_row.append('')
    #         list_row.append('')
    #         list_row.append(int(order.nr_order))
    #         list_row.append('')
    #         list_row.append('')
    #         #print('list row-: ',list_row)
    #         not_damage_list.append(list_row)
    #     values.append(not_damage_list)

    #     for sku in products_list_damage:
    #         list_row = []
    #         list_row.append(date_writes)
    #         list_row.append(sku[0])
    #         list_row.append(return_sku_information(sku[0])['name_of_product'])
    #         list_row.append(sku[1])#кількість продукту
    #         list_row.append('')
    #         list_row.append('')
    #         list_row.append(int(order.nr_order))
    #         list_row.append('')
    #         list_row.append('')
    #         damage_list.append(list_row)
    #     values.append(damage_list)

    # print(values)
    return values

def gswrite(request):
    date_to_print = request.GET.get("date_to_print").replace('-','/').split('/')
    date_to_print = str(date_to_print[2]+'/'+date_to_print[1]+'/'+date_to_print[0])
    date_to_print = datetime.strptime(date_to_print,'%d/%m/%Y')
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

    #datetime_object = datetime.strptime('2022-07-20', "%Y-%m-%d").date()
    list_order_today = Order.objects.filter(date_writes= date_to_print)
    order_products = OrderProduct.objects.filter(date_writes = date_to_print)
    

    values = gen_value_for_gsheet(list_order_today, order_products)
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

    return render(request, 'gen_protocol/home.html')
#zdfjsfjkla