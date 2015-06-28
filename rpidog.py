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
        msg = MIMEMultipart()
        msg.attach(MIMEText('Wykryto ruch! zdjecia: '))
        msg.attach(MIMEImage(file("alarm1.jpg").read()))
        msg.attach(MIMEImage(file("alarm2.jpg").read()))
        msg.attach(MIMEImage(file("alarm3.jpg").read()))

        self.s.sendmail(self.smtpUser, self.addrTo, msg.as_string())

        print ('Email sent!')
        return





def get_file_name():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")




def cam_init():
    cam = picamera.PiCamera()
    cam.resolution = (1920, 1080)
    cam.fps = 30
    cam.start_preview()
    return cam

def PIR_init():
    pir = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir, GPIO.IN, GPIO.PUD_DOWN)
    return pir


cam = cam_init()
pir = PIR_init()
mail = email()

previous_state = False;
current_state = False;

cam.start_preview()

while True:
	time.sleep(0.1)
	previous_state = current_state
	current_state = GPIO.input(pir)

	if current_state != previous_state:

		if current_state:
			print ('Motion detected!')
			cam.start_recording(get_file_name())
			print ('Recording started')
			cam.wait_recording(0.3)
			cam.capture('alarm1.jpg', use_video_port=True)
			print ('Image 1 captured')
                        cam.wait_recording(1)
                        cam.capture('alarm2.jpg', use_video_port=True)
                        print ('Image 2 captured')
                        cam.wait_recording(1)
                        cam.capture('alarm3.jpg', use_video_port=True)
                        print ('Image 3 captured')
			print ('Images captured')
                        cam.start_recording(get_file_name())
                        print ('maile sending...')
			mail.send_email()
		else:
			cam.stop_recording()
			print ('Recording stopped')
			print ('End of motion')
			
