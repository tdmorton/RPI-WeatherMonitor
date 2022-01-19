import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont

x = [0]

plt.plot(x)
plt.savefig("testplot.png")

maxsize = (480,480)

im = Image.new("RGB", (480,800), (255,255,255))
im2 = Image.open("testplot.png")

im2.thumbnail(maxsize, Image.ANTIALIAS)
thresh = 200
fn = lambda x: 255 if x > thresh else 0
im2.convert('L').point(fn,mode="1")
im2.save("tests","PNG")

im.paste(im2,(0,0))
im.save("im.png","PNG")
