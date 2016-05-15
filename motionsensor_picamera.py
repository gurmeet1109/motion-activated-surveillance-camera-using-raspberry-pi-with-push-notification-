import RPi.GPIO as GPIO
import time
import picamera
import datetime  # new
import urllib2
import json
GPIO.setwarnings(False)


def get_file_name():  # new
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

def get_file_name1():  # new
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")

def sendNotification(token, channel, message):
         data = {
                 "body" : message,
                 "message_type" : "text/plain"
                }
         req = urllib2.Request('http://api.pushetta.com/api/pushes/{0}/'.format(channel)) 
         req.add_header('Content-Type', 'application/json')
         req.add_header('Authorization', 'Token {0}'.format(token))
         response = urllib2.urlopen(req, json.dumps(data))

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False

cam = picamera.PiCamera()

while True:
    time.sleep(0.1)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    if current_state != previous_state:
        new_state = "HIGH" if current_state else "LOW"
        print("GPIO pin %s is %s" % (sensor, new_state))
        if current_state:
            print ('motion detected')
            sendNotification("e942e611dc1d985597d26df56ac87dd91ca3349d", "my_sensor", "someone is at door")
            fileName = get_file_name()  # new
            fileName1 = get_file_name1()
            print "about to take picture"
            cam.capture(fileName1)
            print "picture taken"
            print "Starting Recording..."
            cam.start_preview()
            cam.start_recording(fileName)  # new
            print (fileName)
        else:
            cam.stop_preview()
            cam.stop_recording()  # new
            print "Stopped Recording"
