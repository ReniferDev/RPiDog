import RPi.GPIO as GPIO
import time
import picamera
import datetime
import smtplib
import email
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


class email:
 
    def __init__(self):
        self.credentials = open('rpidog.conf', 'r')
        self.smtpUser = self.credentials.readline().replace("username = ", "")
        self.smtpPass = self.credentials.readline().replace("password = ", "")
        self.addrTo   = self.credentials.readline().replace("receiver = ", "")

        self.s = smtplib.SMTP('smtp.gmail.com',587)
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo()

        self.s.login(self.smtpUser, self.smtpPass)
        return
        

    def send_email(self):
        print ('mail sending...')
        msg = MIMEMultipart()
        msg.attach(MIMEText('Wykryto ruch! zdjecia: '))
        msg.attach(MIMEImage(file("/home/pi/RPiDogOutput/Alarms/alarm 0.jpg").read()))
        msg.attach(MIMEImage(file("/home/pi/RPiDogOutput/Alarms/alarm49.jpg").read()))
        msg.attach(MIMEImage(file("/home/pi/RPiDogOutput/Alarms/alarm99.jpg").read()))

        self.s.sendmail(self.smtpUser, self.addrTo, msg.as_string())

        print ('Email sent!')
        return





def get_file_name():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")




def cam_init():
    cam = picamera.PiCamera()
    cam.resolution = (640,480)
    cam.fps = 5
    cam.start_preview()
    time.sleep(2)
    return cam

def cam_high():
    global cam, rect_timer, video_low_profile
    cam.resolution = (1920, 1080)
    cam.fps = 30    
    rec_timer = time.time()   
    vieo_low_profile = False    
    return

def cam_low():
    global cam, rect_timer, video_low_profile
    cam.resolution = (640,480)
    cam.fps = 5    
    rec_timer = time.time()    
    video_low_profile = True    
    return

def save_video():
    global rec_timer
    cam.stop_recording()
    print('Video saved')
    cam.start_recording(get_file_name())
    
    
    rec_timer = time.time()
    
    return

def PIR_init():
    pir = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir, GPIO.IN, GPIO.PUD_DOWN)
    return pir


cam = cam_init()
pir = PIR_init()
mail = email()

previous_state = False
current_state = False
video_low_profile = True

cam.start_recording(get_file_name())
rec_timer = time.time()

while True:
    if video_low_profile:
        if ((time.time() - rec_timer ) > 15):
            save_video()     
    previous_state = current_state
    current_state = GPIO.input(pir)

    if current_state != previous_state:
        if current_state:
            alarm_start = time.time()
            print ('Motion detected')
            cam.stop_recording()
            print ('LOWCAM sopped  ')
            cam_high()
            video_low_profile = False
            cam.capture_sequence(['/home/pi/RPiDogOutput/Alarms/alarm%02d.jpg' %i for i in range(1, 100)], use_video_port=True)
            print ('Images captured on micro ')         
            cam.start_recording('/home/pi/RPiDogOutput/Alarms/' + get_file_name())
            print ('HIGHCAM started ')
            cam.wait_recording(10)
            #mail.send_email()
            cam.stop_recording()
            cam.start_recording('/home/pi/RPiDogOutput/Alarms/' + get_file_name())
            

	else:
	    print ('End of motion  ')
	    cam.stop_recording()
	    print ('HIGHCAM stopped ')
            cam_low()
            video_low_profile = True
	    cam.start_recording(get_file_name())

			
