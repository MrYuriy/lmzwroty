from operator import inv, truediv
from pydoc import cli
from select import select
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Adres
from .serializers import GenadresSerializer
from .models import User
from django.http import HttpResponse
from django.shortcuts import redirect

class GenadresView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        inventory_adreses = request.data['inventory_adreses']
        inventory_qtys = request.data['inventory_qtys']
        adreses = request.data['adreses'] + request.data['adreses_archive'] 
        
        resolt = self.adrese_and_qantity(
            self.inventory_transaction_list(adreses), 
            self.inventory_dict(inventory_adreses,inventory_qtys))   
        return Response({"list_adreses":  resolt}, status=status.HTTP_200_OK)

    def filter(self, adres):
        try:
            adres = str(adres)
            adres = adres.replace('-','')
            if adres=='' or adres == None or len(adres)<=4:
                return False
            # куветки   K*******  K1204503  // вяти      W**** W0123 // карнизи   D**** D1330 
            if adres[0]=='K' or adres[0]=='W' or adres[0]=='D':
                if adres[1:].isdigit():
                    return True
                else:
                    return False

            elif (adres[0:1]=="WK" or adres[0:1]=="WS") and adres[2:].isdigit():
                return True
                    
            # регали    **R****L** 01R2104A10 01R1027A15 01R0517H1
            elif adres!="PARKING" and adres[2]=='R' and adres[7].isalpha():
                if adres[0:2].isdigit() and adres[3:7].isdigit():
                    return True
                else:
                    return False
            # маси      **M*** 01M242   01M525-20 01M316-03
            elif adres[2]=='M':
                if adres[3:].isdigit():
                    return True
                else:
                    return False

            elif adres[:8]=="SZYB-ZAM" :
                return True
            elif adres=='INRACK80':
                return True
            else:
                return False
        except:
            return False

    

    def inventory_transaction_list(self, list_adreses):
        clin_list = []
        if not list_adreses:
            return clin_list  
        for adres in list_adreses:
            if self.filter(adres) and adres not in clin_list:
                clin_list.append(adres)
        return (clin_list)
    
    def inventory_dict(self, adreses,inventory_qtys):
        
        if adreses != [None] and inventory_qtys != [None] :
            
            inventory_dictionary = {}
            for i in range(len(adreses)):
                if adreses[i] in inventory_dictionary:
                    inventory_dictionary[adreses[i]] += int(inventory_qtys[i])
                else:
                    inventory_dictionary[adreses[i]] = int(inventory_qtys[i])
            return (inventory_dictionary)
        return {}

    def adrese_and_qantity(self, adreses_list, inventory_dictionary):
        resolt = []
        if not adreses_list :
            
            #resolt = numpy.array(list(inventory_dictionary.items()))
            for adres, qty in inventory_dictionary.items():
                resolt.append([adres,str(qty)])

            resolt = []

            for adres in inventory_dictionary:
                resolt.append(str(adres)+" - "+str(inventory_dictionary[adres]))

            return resolt
        elif not inventory_dictionary:
            return adreses_list
        else: 
            for adres in adreses_list:
                if adres in inventory_dictionary.keys():
                    #print (adres,inventory_dictionary[adres])
                    resolt.append(str(adres)+" - "+str(inventory_dictionary[adres]))

                else:
                    resolt.append(adres)
            for adres_invent in inventory_dictionary.keys():
                if adres_invent not in adreses_list:
                    resolt.append(str(adres_invent)+" - "+str(inventory_dictionary[adres_invent]))
                    #print(adres)
            return (resolt)
        


def home(request):
    users = User.objects.all()
    
    return render(request, 'genadres/home.html',{"users": users})

def get_sheet(request):
    user_name = request.GET.get('username')
   
    user = User.objects.filter(name=user_name).last()
    
    url = f"https://test-u-murex.vercel.app/?from_location={user.from_location}&to_location={user.to_location}&inventory_adres={user.inventory_adres}&inventory_qty={user.inventory_qty}&from_location_arc={user.from_location_arc}&to_location_arc={user.to_location_arc}"
    return redirect(url)

def create_user(request):
    alphabet = "A B C D E F G H I K L M N O P Q R S T V X Y Z".split()
    user_parametrs = ['from_location', 
                 'to_location', 
                 'inventory_adres', 
                 'inventory_qty', 
                 'from_location_arc', 
                 'to_location_arc']
    return render(
        request, 
        'genadres/add-user.html', 
        {'alphabet':alphabet, "user_parametrs":user_parametrs}
        )


def save_user(request):
    name_area = request.GET.get('user-name')
    from_location_area = request.GET.get('from_location')
    to_location_area = request.GET.get('to_location')

    inventory_adres_area = request.GET.get('inventory_adres')
    inventory_qty_area = request.GET.get('inventory_qty')

    from_location_arc_area = request.GET.get('from_location_arc')
    to_location_arc_area = request.GET.get('to_location_arc')

    

    user = User(
        name = name_area,
        from_location = from_location_area,
        to_location = to_location_area,
        inventory_adres = inventory_adres_area,
        inventory_qty = inventory_qty_area,
        from_location_arc = from_location_arc_area,
        to_location_arc = to_location_arc_area
    )

    user.save()
    return redirect("home_adreses")
    

