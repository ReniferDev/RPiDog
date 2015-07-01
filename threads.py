import RPi.GPIO as GPIO
import time
import picamera
import datetime
import smtplib
import email
import os
import threading
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage


def LowResRecording(id, stop):
    print("Low res recording started", id)
    cam.resolution = (640,480)
    cam.fps = 5
    rec_timer = time.time()
    cam.start_recording(get_file_name())
    while True:
        cam.wait_recording(1)
        if stop():
            cam.stop_recording()
            break
        if ((time.time() - rec_timer ) > 15):
            cam.stop_recording()
            print('Video saved')
            time.sleep(2)
            cam.start_recording(get_file_name())
            rec_timer = time.time() 
            
    print('Low res recording stopped')

def do_work2(id, stop):
    print("I am thread", id)
    while True:
        print("I am thread {} doing something".format(id))
        time.sleep(1)
        if stop():
            print("  Exiting loop.")
            break
    print("Thread {}, signing off".format(id))


def cam_init():
    cam = picamera.PiCamera()
    cam.resolution = (640,480)
    cam.fps = 5
    cam.start_preview()
    time.sleep(2)
    return cam

cam = cam_init()

def main():
    stop_thread1 = False
    #stop_thread2 = False
    workers = []

    tmp1 = threading.Thread(target=do_work1, args=(1, lambda: stop_thread1))
    workers.append(tmp1)
    #tmp2 = threading.Thread(target=do_work1, args=(2, lambda: stop_thread2))
    #workers.append(tmp2)
    tmp1.start()
    #tmp2.start()
    
    time.sleep(65)
    print('main: closing thread 1')
    stop_thread1 = True

    #time.sleep(3)
    #print('main: closing thread 2')
    #stop_thread2 = True
    
    for worker in workers:
        worker.join()
    print('Finish.')
    return

main()
