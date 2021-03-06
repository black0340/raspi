from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.shortcuts import render,HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SavedImage
from .serializers import SavedImageSerializer,MySerializer
import cv2
import threading
import RPi.GPIO as GPIO
import time
import imutils
import webbrowser
import os,time
import pyautogui

videosave = 0
savetimer = 0
distance = 0
Trig = 11
Echo = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)


def ImageSave(image, distance):
    imgCount = SavedImage.objects.count()
    cv2.imwrite(f'live/static/savedimage/{str(imgCount)}.png',image,params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    savedimage = SavedImage(UltraSonic=distance,ImageNumber=imgCount)
    savedimage.save()
    return imgCount

def controlUltra():

    global videosave,savetimer
    pulse_start=time.time()
    pulse_end =time.time()
    GPIO.setwarnings(False) 
    global distance
    GPIO.output(Trig,GPIO.LOW)
    time.sleep(0.005)
    GPIO.output(Trig,GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(Trig,GPIO.LOW)
    while GPIO.input(Echo) == 0:
        pulse_start=time.time()
    while GPIO.input(Echo) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance,2)
    if distance<20 and savetimer >20:
        videosave = 1
        print(distance)
    savetimer += 1
    return distance
    
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        global videosave,savetimer
        while True:
            threading.Thread(target=controlUltra).start()
            if videosave==1 and savetimer >20:
                print('image saved')
                videosave=0
                savetimer =0
                ImageSave(self.frame,distance)
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try: 
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
def streaming(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def main_loged_in(request):
    return render(request,'main_loged_in.html')

def savedimg(request, imgNum):
    savedimage = SavedImage.objects.filter(ImageNumber=imgNum)
    context = savedimage.values()[0]
    print(context)
    return render(request,'savedimg.html',context)

@api_view(['GET'])
def dbserial(request):
    savedimage = SavedImage.objects.filter(ImageNumber=3)
    imgserial = SavedImageSerializer(savedimage[0])
    return Response(imgserial.data)

@api_view(['GET'])
def myserial(request):
    savedimage = SavedImage.objects.all()
    imgserial = MySerializer(savedimage,many=True)
    print(imgserial.data)
    
    url = "https://www.youtube.com/embed/lL7YiUr7-8U?autoplay=1&mute=1"
    webbrowser.open(url)
    
    return Response(imgserial.data)

def videourl(request, url):
    openurl = "https://www.youtube.com/embed/"+url+"?autoplay=1"
    webbrowser.open(openurl)
    time.sleep(3)
    pyautogui.click(x=1146,y=1061)
    return Response(url+" play")
    
def urlget(request):
    return render(request,"urlget.html")

def gall(request):
    i = SavedImage.objects
    return render(request, "gall.html",{'i':i})