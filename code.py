# -*- coding:utf-8 -*-
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random

def create():
    def char():
        # create random char
        return chr(random.randint(65,90))

    def background_color():
        # create random color
        color_background = (random.randint(64,255), random.randint(64,255), random.randint(64,255))
        return color_background

    def txt_color():
        color_txt = (random.randint(32,127), random.randint(32,127), random.randint(32,127))
        return color_txt

    list = []
    width = 60*4
    height = 60
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('Keyboard.ttf', 36)
    for x in range(width):
        for y in range(height):
            draw.point((x,y), fill=background_color())
    for t in range(4):
        str = char()
        list.append(str)
        draw.text((40*t+10,5), str, font=font, fill=txt_color())

    params = (1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500,
    )
    img = img.transform(img.size, Image.PERSPECTIVE, params)
    image = img.filter(ImageFilter.BLUR)
    return image, ''.join(list)
