#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import Adafruit_DHT
import matplotlib.pyplot as plt

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

logging.basicConfig(level=logging.DEBUG)

print('before instantiation')

temps_bavg = []
hums_bavg = []
templist = []
humlist = []

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()

    logging.info("init and Clear")

    font50 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 37)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    #font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    #font37 = ImageFont.truetype(os.path.join(picdir, 'Font.tcc'), 37)

    while True:
        epd.init()
        epd.Clear()
        print('before for')
        for x in range(10):
            print('in for')
            humi, tempe = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            print('after temp  read')
            temps_bavg.append(tempe)
            hums_bavg.append(humi)
            print(x)
        temperature = sum(temps_bavg)/len(temps_bavg)
        humidity = sum(hums_bavg)/len(hums_bavg)

        str1 = str(round(temperature,1))+" "+ u'\N{DEGREE SIGN}' + "C"
        str2 = str(round((temperature*1.8+32),1))+" " + u'\N{DEGREE SIGN}' + "F"
        str3 = str(round(humidity, 1))
        str4 = str1 + "  " + str2 + "  " + str3 + "%"


        # Drawing on the Vertical image
        logging.info("2.Drawing on the Vertical image...")
        Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        draw.text((15, 15), 'RPI Temperature Logger', font = font24, fill = 0)
        draw.text((15, 50), "Temperature Inside", font = font24, fill = 0)
        draw.text((15, 85), str4, font = font50, fill = 0)
        draw.text((15, 155), 'Temperature Outside',font = font24, fill = 0)
        draw.text((15, 190), str(round(temperature,1)+10), font = font50, fill = 0)
        epd.display(epd.getbuffer(Limage))

        logging.info("4.read bmp file on window")
        #Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        templist.append(round(temperature,1))
        if len(templist) > 72:
            templist.pop(0)
        humlist.append(round(humidity,1))
        if len(humlist) > 72:
            humlist.pop(0)

        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open("temps.txt", "a") as output:
            output.write(str(round(temperature,1)) + ", " + str(round(humidity,1)) + ", " + timestr)

        plt.clf()
        plt.plot(templist)
        plt.savefig('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/tempplot.png')
        maxsize = (480,480)

        im1 = Image.new("RGB",(480,480),(255,255,255))
        im2 = Image.open('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/tempplot.png')

        im2.thumbnail(maxsize, Image.ANTIALIAS)
        thresh = 200
        fn = lambda x: 255 if x > thresh else 0
        im2.convert("L").point(fn,mode="1")
        im2.save(os.path.join(picdir,'image1.png'))

        bmp = Image.open(os.path.join(picdir, 'image1.png'))
        Limage.paste(bmp, (0,320))
        epd.display(epd.getbuffer(Limage))
        time.sleep(2)

        #logging.info("Clear...")
        #epd.init()
        #epd.Clear()

        logging.info("Goto Sleep...")
        epd.sleep()
        time.sleep(600)

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
