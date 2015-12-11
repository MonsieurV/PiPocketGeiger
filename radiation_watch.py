import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def onRadiation(c):
	print("Raddon!")

GPIO.add_event_detect(24, GPIO.FALLING, callback=onRadiation)

try:
	while(1):
		pass
finally:
	GPIO.cleanup()
