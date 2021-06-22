
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from django.template import loader
# from django.db import models

from pricetagapp.models import *

#from .models import Skanaction
#from .models import Tasks

import logging
import requests
import json
import base64
from pyzbar.pyzbar import decode
from io import BytesIO
from PIL import Image
import base64
from pathlib import Path




logger = logging.getLogger(__name__)

def index(request):

    tasks = Actualtask.objects.all()
    leaders = Leaderboard.objects.all()

    return render(request, "index.html",{'tasks':tasks,'leaders':leaders})

def makemagic(request):

    #получаем картинку
    imgurl = request.body
    

    #получаем цену с ценника
    ocr_price = ocr_space_file(filename='recievedIMG.png', imgurl=imgurl, language='rus')
    #ocr_price = 101

    print('ocr price:',ocr_price)

    #получаем ид товара с ценника
    ocr_sku = getcodevalue(imgurl,'EAN13')
    #ocr_sku = 1

    print('ocr_sku:',ocr_sku)

    status = 'u'
    if ocr_price is None or ocr_sku is None:
        status = 'bad image'
    
    

    if status != 'bad image':
    #сохраняем сканирование
    #юзер считаем у нас один
        sa = Scanaction(sku=ocr_sku,price=ocr_price,user_id=1)
        sa.save()

        #получаем актуальную цену
        actual_price=getactualprice(ocr_sku)
        print('actual_price:',actual_price)

        if ocr_price == actual_price:
            Tasks.objects.filter(sku=ocr_sku).delete()
            status='ok'
            #HttpResponse('ok')
        else:
            
            t = Tasks.objects.filter(sku=ocr_sku)
            if not t:
                t = Tasks(sku=ocr_sku,tasktype='Обновить ценник')
                t.save()

            status='not ok'

    print(status)

    t = list(Actualtask.objects.all().values())
    l = list(Leaderboard.objects.all().values())
    print(t)

    return JsonResponse({'status':status,'tasks':t,'leaders':l})

def getcodevalue(imgurl,codetype):
    img_data = imgurl.decode('utf-8').replace('data:image/png;base64,', '')

    
    im = Image.open(BytesIO(base64.decodebytes(img_data.encode())))
    im.save(fp=r'recievedIMG_codecode.png')

    d = decode(im)

    print('ocrid:',d)

    for dd in d:
        if dd.type == codetype:
            return dd.data.decode('utf-8')
        else:
            pass


def getactualprice(ocr_sku):
    return 100

def ocr_space_file(filename, imgurl, overlay=False, api_key='b3d764d35e88957', language='rus'):
    CORRECT_PRICE = 66500
    
    crop_image(imgurl=imgurl)

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

        #d = r.json()
        #a = d['ParsedResults'][0]['ParsedText']

        #print('rp parsed text:',a)

        result = r.content.decode()
        res_array = json.loads(json.dumps(result))

        print(res_array)

        actual_price = int(res_array.split(',')[5].replace('"ParsedText":"', '').replace(' ', ''))

        print('CORRECT PRICE =', CORRECT_PRICE, '\n', 'ACTUAL PRICE =', actual_price)
        if actual_price == CORRECT_PRICE:
            print('----------------------Все четко:)----------------------')
        else:
            print('----------------------Надо менять!----------------------')

        if actual_price:
            return actual_price
        else:
            return None


def crop_image(imgurl):

    img_data = imgurl.decode('utf-8').replace('data:image/png;base64,', '')

    im = Image.open(BytesIO(base64.decodebytes(img_data.encode())))

    width, height = im.size

    # Setting the points for cropped image
    left = 190
    top = height / 1.6
    right = 500
    bottom = 1.6 * height / 2

    image_cropped = im.crop((left, top, right, bottom))

    image_cropped.save(fp=r'recievedIMG.png')


