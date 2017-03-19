#-------------------------------------------------常用的第三方模块
#所有第三方的包都会被pip安装到Python3的site-packages目录下
#基本上，所有的第三方模块都会在PyPI - the Python Package Index上注册，只要找到对应的模块名字，即可用pip安装。


#-------------------------------------------------PIL
#PIL:python image Library
#pillow
#命令行中安装pillow：pip install pillow，如果遇到Permission denied安装失败，请加上sudo重试
#操作图像，做到图像缩放
from PIL import Image

# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.jpg')
# 获得图像尺寸:
w, h = im.size
print('Original image size: %sx%s' % (w, h))
# 缩放到50%:
im.thumbnail((w//2, h//2))
print('Resize image to: %sx%s' % (w//2, h//2))
# 把缩放后的图像用jpeg格式保存:
im.save('thumbnail.jpg', 'jpeg')

#增加模糊效果
im2 = im.filter(ImageFilter.Blue)
im2.save('blue.jpg','jpeg')

##生成验证码，利用PIL的ImageDraw的绘图功能·
from PIL import Image,ImageDraw,ImageFont,ImageFilter		#滤镜

import random
#随机字母
def rndChar():
	return chr(random.randint(65,90))

#随机颜色1：
def rndColor():
	return (random.randint(64,255),random.randint(64,255),random.randint(64,255))	#rgb

#随机颜色2：
def rndColor2():
	return (random.randint(32,127),random.randint(32,127),random.randint(32,127))	#rgb

# 240 x 60:
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 36)  		#所有字体都是操作系统管理的，其实就是一个几M的大文件。Python没有自带的字体

# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素:
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor())
# 输出文字:
for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
# 模糊:
image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')