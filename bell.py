from gpiozero import Button, LED
import fbchat
import time
from fbchat.models import *
from signal import pause
import datetime
import urllib.request
import cv2
import numpy as np

def BellButtonPressedEvent():
	bell.blink(3,2,2)
	print('Bell button pressed')
	SendMessage('Niekto zvoní',True)

def SendMessage(txt, sendImage=False):
	global client
	threadId = '1088463509'
	threadType = ThreadType.USER
	message_text = str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")+' - '+txt)
	print("sending message...")
	if (sendImage):
		file =  CaptureFrontCamera()
		client.sendLocalFiles(file,Message(text=message_text),thread_id=threadId,thread_type = threadType)
		return
	print('message was sent')
	client.send(Message(text=message_text),thread_id=threadId,thread_type = threadType)

def CaptureFrontCamera():
	_bytes = bytes()
	stream = urllib.request.urlopen('http://192.168.0.51/video.cgi?resolution=1920x1080')
	while True:
		_bytes += stream.read(1024)
		a = _bytes.find(b'\xff\xd8')
		b = _bytes.find(b'\xff\xd9')
		if a != -1 and b != -1:
			jpg = _bytes[a:b+2]
			_bytes = _bytes[b+2:]
			filename = '/home/pi/capture.jpeg'
			i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
			cv2.imwrite(filename, i)
			return filename

bell = LED(18)
bellButton = Button(6)
bellButton.when_pressed = BellButtonPressedEvent

print('Preparing connection to Facebook messenger...')
client = fbchat.Client('alica.homeguard@protonmail.com','pankodankojonatanko')
if client.isLoggedIn():
	print('I am ready...')
	SendMessage('Ahoj môj pane! \nZvonček je pripravený')
pause()
