import RPi.GPIO as GPIO
import time
import picamera
import datetime
import smtplib
import email
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
        msg.attach(MIMEImage(file("alarm 0.jpg").read()))
        msg.attach(MIMEImage(file("alarm49.jpg").read()))
        msg.attach(MIMEImage(file("alarm99.jpg").read()))

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

def cam_high(video_low_profile, cam, rec_timer):
    video_low_profile = False
    cam.resolution = (1920, 1080)
    cam.fps = 30
    rec_timer = time.time()

def cam_low(video_low_profile, cam, rec_timer):
    video_low_profile = True
    cam.resolution = (640,480)
    cam.fps = 5
    rec_timer = time.time()

def save_video(rec_timer):
    cam.stop_recording()
    cam.start_recording(get_file_name())
    rec_timer = time.time()

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
    if ((time.time() - rec_timer ) > 5) and (video_low_profile==True):
        print('About to save: ')
        save_video(rec_timer)
        print('Video saved')
            
    previous_state = current_state
    current_state = GPIO.input(pir)

    if current_state != previous_state:

        if current_state:
            alarm_start = time.time()
            print ('Motion detected')
            print ('stop recording inside loop')
            cam.stop_recording()
            print ('LOWCAM sopped  ')
            cam_high(video_low_profile, cam, rec_timer)
	    cam.capture_sequence(['alarm%02d.jpg' %i for i in range(1, 100)], use_video_port=True)
            print ('Images captured  ')
            #cam.start_recording(get_file_name())
            #print ('HIGHCAM started  '+ ": %s seconds " % (time.time() - timer))
            #cam.wait_recording(5)
            #cam.stop_recording()
            #print('HIGHCAM stopped  '+ ": %s seconds " % (time.time() - timer))
	    #mail.send_email()
            time.sleep(5)            
	else:
	    print ('End of motion  ')
            cam_low(video_low_profile, cam, rec_timer)
	    cam.start_recording(get_file_name())

			
