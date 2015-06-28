import RPi.GPIO as GPIO
import time
import picamera
import datetime
import smtplib

smtpUser = 'XXX@gmail.com'
smtpPass = 'YYY'

addrTo = 'bartek.renifer@gmail.com'
addrFrom = smtpUser

subject = 'Alarm!'
header = 'To: ' +addrTo + '\n' + 'From: ' +addrFrom + '\n' + 'Subject: ' + subject 
body = 'Wykryto ruch! zdjecie: '

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

s = smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()
s.login(smtpUser, smtpPass)

def get_file_name():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False;
current_state = False;

cam = picamera.PiCamera()
cam.resolution = (1920, 1080)
cam.start_preview()

while True:
	time.sleep(0.1)
	previous_state = current_state
	current_state = GPIO.input(sensor)
	if current_state != previous_state:
		new_state = "HIGH" if current_state else "LOW"
		print("PIR State:  %s" % (new_state))	
		if current_state:
			print 'Motion detected!'
			fileName = get_file_name()
			cam.start_recording(fileName)
			cam.wait_recording(0.1)
			print 'Recording started'  
			cam.capture('alarm.jpg',use_video_port=True)
			cam.capture('alarm2.jpg',use_video_port=True)
			cam.capture('alarm3.jpg',use_video_port=True)
			print 'Images captured'
			cam.wait_recording(5)

			msg = MIMEMultipart()
			msg.attach(MIMEText('Wykryto ruch! zdjecie: '))
			msg.attach(MIMEImage(file("alarm.jpg").read()))
			msg.attach(MIMEImage(file("alarm2.jpg").read()))
			msg.attach(MIMEImage(file("alarm3.jpg").read()))
			s.sendmail(addrFrom, addrTo, msg.as_string())
			print 'Email sent!'
						
		else:
			cam.stop_recording()
			print 'Recording stopped'
			print 'End of motion'
			
