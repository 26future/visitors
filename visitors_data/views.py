from django.shortcuts import render, redirect
from .models import Visitor
import qrcode
from .forms import VisitorForm
import cv2
import re
# from IPython import embed
from django.http import JsonResponse

# Create your views here.

def home(request):
    context = {

    }
    return render(request, 'visitors_data/home.html', context)

def new(request): # POST
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            # visitor = form.save()
            visitor = form.save()
            return redirect('visitors_data:confirm', visitor.pk)
    else:
        form = VisitorForm()
    context = {
        'form': form,
    }
    return render(request, 'visitors_data/new.html', context)

## https://docs.djangoproject.com/en/3.0/ref/contrib/messages/    => error message custom

def new_en(request): # POST
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     number = request.POST.get('number')

    #     visitor = Visitor(name=name, number=number)
    #     visitor.save()
    
    #     return redirect('visitors_data:detail', visitor.pk)

    # else:
    context = {

    }
    return render(request, 'visitors_data/new_en.html', context)

def confirm(request, pk):
    visitor = Visitor.objects.get(pk=pk)
    context = {
        'visitor': visitor,

    }
    
   
    return render(request, 'visitors_data/confirm.html', context)

def qr(request, pk):
    visitor = Visitor.objects.get(pk=pk)
    qr = qrcode.QRCode(version=2, box_size=5, error_correction=qrcode.constants.ERROR_CORRECT_H)
    info = visitor.name + '/' + visitor.number + '/' + 'PK:' + str(visitor.pk)
    qr.add_data(info)
    qr.make
    img = qr.make_image(fill_color='black', back_color='white')
    img.save('./static/images/qrcode.png', format='PNG')

    return render(request, 'visitors_data/qr.html')


def read_qr(request):

    context = {

    }
    return render(request, 'visitors_data/read_qr.html',context)




def create_qr(request):
    personal_info = request.POST.get('content')

    p = re.compile("P+K+[:]+[0-9]+")
    pk_number = int(p.findall(personal_info)[0][3:])
    
    visitor = Visitor.objects.get(pk=pk_number)
    visitor.check = "TRUE"
    
    if visitor.check == "FALSE":
        print('신규 방문자')
        visitor.check = "TRUE"
        visitor.save()
    # 재방문자
    else:
        print('재방문자')
        visitor.save()

    # context = {
    #     'context': context
    # }
    return redirect('visitors_data:result')


def result(request):
    return render(request, 'visitors_data/make_crop_image.html')


def make_crop_image(request):
    return render(request, 'visitors_data/make_crop_image.html')


def get_crop_image(request):
    crop_image = request.POST.get('image')
    # # embed()
    # # print(crop_image)


    # url = 'crop_image'

    # response = requests.get(url)

    # soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # image = soup.find('img')
    # image_url = image['src']


    # img = Image.open(requests.get(image_url, stream = True).raw)

    # img.save('test_image.jpg')



    return redirect('visitors_data:home')