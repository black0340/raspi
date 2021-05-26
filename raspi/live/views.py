from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.shortcuts import render
import cv2
import threading
import RPi.GPIO as GPIO
import time
import imutils

videosave = 0
savetimer = 0
Trig = 11
Echo = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)


def controlUltra():

    global videosave,savetimer
    pulse_start=time.time()
    pulse_end =time.time()
    GPIO.setwarnings(False) 
    distance=0.0
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
    if distance>50 and savetimer >20:
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
                cv2.imwrite('p2.png',self.frame,params=[cv2.IMWRITE_PNG_COMPRESSION,0])
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
def index(request):
    return render(request,'index.html')

