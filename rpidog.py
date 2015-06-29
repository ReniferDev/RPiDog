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
        msg.attach(MIMEImage(file("alarm 9.jpg").read()))
        msg.attach(MIMEImage(file("alarm 19.jpg").read()))

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
cam.start_recording(get_file_name())
time.sleep(2)

while True:
	previous_state = current_state
	current_state = GPIO.input(pir)

	if current_state != previous_state:

		if current_state:
                        print ('Motion detected')
                        cam.stop_recording()
			cam.capture_sequence(['alarm%2d.jpg' % i for i in range(20)], use_video_port=True)
                        print ('10 Images captured')
                        cam.start_recording(get_file_name())
                        cam.wait_recording(5)
                        cam.stop_recording()                       
			mail.send_email()
			cam.start_recording()
		else:
			print ('End of motion')
			
