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

from PIL import Image
from PIL import Image, ImageDraw

from twython import Twython

segments =  (26,19,13,21,20,16,12) #ABCDEFG pins for the 7 segment display

 
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
 
digits = (22,27,17,24)
 
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0),   #dictionary of all possible numbers that could be displayed
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
 
def button_callback(channel): #function is called when it detects the button push
   
    for i in range(4):
        time.sleep(3) #short delay before the countdown so you have some time to pick a pose!
        n = 321       # display counts down from 3, 2, then 1, before snapping a photo
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
        camera.capture('/home/lieumelvin/Pictures/Image ' + str(i) + '.jpg') #photos taken are saved into a folder
        camera.stop_preview()        
   
   
    imageList = []
    Logo = Image.open("/home/lieumelvin/Pictures/SuLogo.png") #Seattle University logo is saved in the same folder as photos
    Logo = Logo.resize((100, 100))
   
    for i in range(4):
        imageList.append(Image.open("/home/lieumelvin/Pictures/Image %s.jpg" % i).resize((480,480)))
        
         #photos are retrieved and resized, and appended to an empty list
   
    Image01 = imageList[0]
    Image02 = imageList[1]
    Image03 = imageList[2]
    Image04 = imageList[3]


    newImage = Image.new("RGB", (2000, 500), (0, 0, 0) )

    for p in range(4):
        newImage.paste(imageList[p], (p*500,0))    #photos are stitched horizontally, side by side, "photo booth" style
   
    newImage.paste(Logo,(1880,380))     #logo is inserted in bottom right corner of photo strip

    draw = ImageDraw.Draw(newImage) #border is drawn from PIL library around pictures
    draw.line((0, 0, 0, 500), fill = (0, 0, 0), width = 40)
    draw.line((0, 0, 2000, 0), fill = (0, 0, 0), width = 40)
    draw.line((2000, 0, 2000, 500), fill = (0, 0, 0), width = 40)
    draw.line((0, 500, 2000, 500), fill = (0, 0, 0), width = 40)

    newImage.save("/home/lieumelvin/Pictures/Saved.jpg")
   
    C_key = "LJgGfPOYX1UGRXmKZ423ynLAB"    #sudo access to keys to automatically upload finished product to Twitter account
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
        time.sleep(1e61)
           
finally:
   
    GPIO.cleanup()

