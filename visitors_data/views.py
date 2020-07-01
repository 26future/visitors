from django.shortcuts import render, redirect
from .models import Visitor
import qrcode
from .forms import VisitorForm
import cv2
import re
from django.http import JsonResponse
import os
from PIL import Image
# from IPython import embed


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
    return render(request, 'visitors_data/read_qr.html')

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
    # return redner(request, 'articles/index.html', context)
    return redirect('visitors_data:result', visitor.pk)


def result(request, visitor_pk):
    visitor = Visitor.objects.get(pk=visitor_pk)
    context = {
        'visitor': visitor,
    }
    return render(request, 'visitors_data/result.html', context)


def make_crop_image(request):
    return render(request, 'visitors_data/make_crop_image.html')

def get_crop_image(request):
    crop_image = request.POST.get('image')
    # print(crop_image)
    # time.sleep(2)
    if len(crop_image) >= 10:
        path = 'C:/Users/student/Downloads/'

        # each_file_path_and_gen_time: 각 file의 경로와, 생성 시간을 저장함
        each_file_path_and_gen_time = []
        for each_file_name in os.listdir(path):
            # getctime: 입력받은 경로에 대한 생성 시간을 리턴
            each_file_path = path + each_file_name
            each_file_gen_time = os.path.getctime(each_file_path)
            each_file_path_and_gen_time.append(
                (each_file_path, each_file_gen_time)
            )

        # 가장 생성시각이 큰(가장 최근인) 파일을 리턴 
        most_recent_file = max(each_file_path_and_gen_time, key=lambda x: x[1])[0][2:]
        # 이미지 열기
        print("가장 최근에 생성된 파일 : "+most_recent_file)
        im = Image.open(most_recent_file)
        cnt = 0
        tmp = []
        for i in most_recent_file:
            cnt+=1
            if i in '/':
                tmp.append(cnt)
        file_name = most_recent_file[tmp[-1]:]
        print(file_name)
        area = (190,113,440,370)
        im = im.crop(area)
        im = im.resize((224,224))
        im.save('./static/images/'+file_name)
        # os.remove(most_recent_file)
        # im.save('')
        # # 이미지 png로 저장
        # im.save('../tmp/tmp.png')
    
    
    # # embed()
    # # print(crop_image)
    # fileName = '../tmp/test.png'
    # req = requests.get(crop_image)
    # file = open(fileName, 'wb')
    # for chunk in req.iter_content(100000):
    #     file.write(chunk)
    # file.close()
    return redirect('visitors_data:home')
