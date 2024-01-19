import os
import textwrap
import sys

from datetime import datetime
from datetime import timedelta
from glob import glob
from random import randrange
from PIL import Image, ImageDraw, ImageFont, ImageOps

from waveshare_epd import epd7in5_V2 as epd7in5

def getTimeQuotes(currentTime,depth):
	hour_minute = currentTime.strftime('%H%M')

	firstTry = True
	if depth > 0:
		firstTry = False

	quotes_path = 'images/metadata/quote_%s_*_credits.png' % hour_minute
	quotes = glob(quotes_path)
	# if len(quotes) == 0:
	# 	# print("No quotes for "+hour_minute)

	# 	# Call the same request, but 1 minute ago
	# 	return getTimeQuotes(currentTime-timedelta(minutes=1),depth+1)
	# else:
		# print("Got quote for "+hour_minute)
	return quotes, firstTry


def main():
	image = Image.new(mode='1', size=(800, 480), color=255)
	now = datetime.now()

	quotes,firstTry=getTimeQuotes(now,0)

	# Write the quote to screen
	quote = quotes[randrange(0, len(quotes))]
	quoteImage = Image.open(quote).convert('1')
	image.paste(quoteImage, (0, 80))

	# If not our first try, also write the current time
	#if not firstTry:
	now_time = now.strftime('%I:%M %p')
	draw_time = ImageDraw.Draw(image)
	time_font = ImageFont.truetype('Literata72pt-Regular.ttf', 48)
	draw_time.text((640, 0), now_time, font=time_font, fill=0)

	today = now.strftime('%a, %B, %d')
	dayFont = ImageFont.truetype('Literata72pt-Regular.ttf', 48)
	drawImage = ImageDraw.Draw(image)
	drawImage.text((10, 0), today, font=dayFont, fill=0)
	drawImage.line([(0, 78), (800, 78)], fill=0, width=2)
	#drawImage.line([(225, 0), (225, 78)], fill=0, width=4)
	return image

if __name__ == '__main__':
	image = main()
	try:
		epd = epd7in5.EPD()
		epd.init()
		if datetime.now().minute == 0 and datetime.now().hour == 2:
			epd.Clear()
		epd.display(epd.getbuffer(image))
		epd.sleep()
	
	except IOError as e:
		print(e)
	
	except KeyboardInterrupt:
		epd.sleep()