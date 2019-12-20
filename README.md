# Photobooth-Code

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False) #for the push button
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN) ##

from picamera import PiCamera #for the camera
from time import sleep 
camera = PiCamera()
camera.rotation = 180
from picamera import PiCamera, Color ##

from PIL import Image #for stitching/drawing/adding images onto photobooth strip
from PIL import Image, ImageDraw ##

from twython import Twython

segments =  (26,19,13,21,20,16,12) #ABCDEFG pins for 7 segment display

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
digits = (22,27,17,24)
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1)}
 
def button_callback(channel): #function is called when the button push is detected
   
    for i in range(4): 
        time.sleep(3) #short pause before the countdown begins, some time to pose!
        n = 321 #what is shown on the 7 segment display
        s = str(n).rjust(4)
        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(segments[loop], num[s[digit]][loop])
           
            GPIO.output(digits[digit], 0)
            time.sleep(1)
            GPIO.output(digits[digit], 1)
         
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
        sleep(2)
        camera.capture('/home/lieumelvin/Pictures/Image ' + str(i) + '.jpg') #images saved into folder
        camera.stop_preview()        
   
   
    imageList = []
    Logo = Image.open("/home/lieumelvin/Pictures/SuLogo.png") #logo saved into same folder as the images that were taken
    Logo = Logo.resize((100, 100))
   
    for i in range(4):
        imageList.append(Image.open("/home/lieumelvin/Pictures/Image %s.jpg" % i).resize((480,480))) 
         
   
    Image01 = imageList[0] #the photos that were saved are then resized, then retrieved
    Image02 = imageList[1]
    Image03 = imageList[2]
    Image04 = imageList[3]


    newImage = Image.new("RGB", (2000, 500), (0, 0, 0) )

    for p in range(4):
        newImage.paste(imageList[p], (p*500,0)) #photos are stitched side by side horizontally
   
    newImage.paste(Logo,(1880,380))

    draw = ImageDraw.Draw(newImage) #border is drawn around the stitched photos
    draw.line((0, 0, 0, 500), fill = (0, 0, 0), width = 40)
    draw.line((0, 0, 2000, 0), fill = (0, 0, 0), width = 40)
    draw.line((2000, 0, 2000, 500), fill = (0, 0, 0), width = 40)
    draw.line((0, 500, 2000, 500), fill = (0, 0, 0), width = 40)

    newImage.save("/home/lieumelvin/Pictures/Saved.jpg")
   
    C_key = "LJgGfPOYX1UGRXmKZ423ynLAB" #sudo developer access to upload finished product automatically to twitter
    C_secret = "1bXDsEVnNTnXbcRi4cC83HpFPD5f3YDK4Tfmnv1G3XErmFq9Wr"
    A_token = "954554405457608704-qsuMlDgxhuxKlBvS1XDDdBz5A2XunBd"
    A_secret = "BGH8M1XoL8v0KaK4Qc1h5SZTL939Az6mV7tKQ9sDZpges"
    myTweet = Twython(C_key,C_secret,A_token,A_secret)
    photo = open('/home/lieumelvin/Pictures/Saved.jpg', 'rb')
    response = myTweet.upload_media(media=photo)
    myTweet.update_status(status='Checkout this cool image!', media_ids=[response['media_id']])
   
GPIO.add_event_detect(4, GPIO.FALLING, callback=button_callback, bouncetime=300)            

try:
    while(1):
        time.sleep(1e6)
           
finally:
   
    GPIO.cleanup()

