import RPi.GPIO as GPIO
from time import sleep
pwm_pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwm_pin, GPIO.OUT)
pwm=GPIO.PWM(pwm_pin, 50)
pwm.start(0)
def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(pwm_pin, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(pwm_pin, False)
	pwm.ChangeDutyCycle(0)
SetAngle(90)
sleep(7)
SetAngle(0)
sleep(7)
SetAngle(-90)
