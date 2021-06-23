
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from django.template import loader

from pricetagapp.models import *

import logging
import requests
import json
import base64
from pyzbar.pyzbar import decode
from io import BytesIO
from PIL import Image,ImageFilter
import base64
from pathlib import Path




logger = logging.getLogger(__name__)

def login(request):
    return render(request, "login.html")
def index(request):

    tasks = Actualtask.objects.all()
    leaders = Leaderboard.objects.all()

    return render(request, "index.html",{'tasks':tasks,'leaders':leaders})

def makemagic(request):

    #получаем картинку
    imgurl = request.body


    #получаем цену с ценника
    ocr_price = ocr_space_file(filename='recievedIMG.png', imgurl=imgurl)
    

    print('ocr price:',ocr_price)

    #получаем ид товара с ценника
    ocr_sku = getcodevalue('recievedIMG_orig.png','QRCODE')
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
    print(l)

    return JsonResponse({'status':status,'tasks':t,'leaders':l})

def getcodevalue(imgurl,codetype):
    

    im = Image.open(imgurl)

    d = decode(im)
    s=''
    print('ocrid:',d)

    for dd in d:
        if dd.type == codetype:
            s = dd.data.decode('utf-8')
        else:
            pass

    if 'eldorado' in s:
        return s.partition('detail/')[2].partition('/')[0]
    else:
        return None


def getactualprice(ocr_sku):
    s = Sku.objects.get(sku=ocr_sku)
    return s.price

def ocr_space_file(filename, imgurl, overlay=False, api_key='b3d764d35e88957'):
    
    
    crop_image(imgurl=imgurl)

    OCREngine = 2
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               # 'language': language,
               'OCREngine':OCREngine,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,

                          )

    d = r.json()
    a = d['ParsedResults'][0]['ParsedText']

    print('ParsedText:',a)

    b = a.split('\n')

    for bb in b:
        bb = bb.replace(' ','')
        print(bb,bb.isnumeric())
        if bb.isnumeric():
            price = int(bb)
            return price
        else:
            price = None
    return price


def crop_image(imgurl):

    img_data = imgurl.decode('utf-8').replace('data:image/png;base64,', '')

    im = Image.open(BytesIO(base64.decodebytes(img_data.encode())))

    im.save(fp=r'recievedIMG_orig.png')
    image_cropped = im.filter(ImageFilter.BoxBlur(3))

    image_cropped.save(fp=r'recievedIMG.png')


