import RPi.GPIO as GPIO
import job01_hardware_setup as hs

def forward_l(speed_l):
    GPIO.output(hs.IN1, GPIO.HIGH)
    GPIO.output(hs.IN2, GPIO.LOW)
    hs.pwm_l.ChangeDutyCycle(speed_l)

def forward_r(speed_r):
    GPIO.output(hs.IN3, GPIO.HIGH)
    GPIO.output(hs.IN4, GPIO.LOW)
    hs.pwm_r.ChangeDutyCycle(speed_r)

def backward_l(speed_l):
    GPIO.output(hs.IN1, GPIO.LOW)
    GPIO.output(hs.IN2, GPIO.HIGH)
    hs.pwm_l.ChangeDutyCycle(speed_l)
    
def backward_r(speed_r):
    GPIO.output(hs.IN3, GPIO.LOW)
    GPIO.output(hs.IN4, GPIO.HIGH)
    hs.pwm_r.ChangeDutyCycle(speed_r)
    
def stop():
    GPIO.output(hs.ENA, GPIO.LOW)
    GPIO.output(hs.ENB, GPIO.LOW)



