import RPi.GPIO as GPIO

ENA = 12
IN1 = 3
IN2 = 4
ENB = 13
IN3 = 15
IN4 = 18
TRIG_r = 17
ECHO_r = 27
TRIG_m = 23
ECHO_m = 24
TRIG_l = 25
ECHO_l = 8

def setup_hardware():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(TRIG_r, GPIO.OUT)
    GPIO.setup(ECHO_r, GPIO.IN)
    GPIO.setup(TRIG_m, GPIO.OUT)
    GPIO.setup(ECHO_m, GPIO.IN)
    GPIO.setup(TRIG_l, GPIO.OUT)
    GPIO.setup(ECHO_l, GPIO.IN)

    global pwm_l, pwm_r
    pwm_l = GPIO.PWM(ENA, 100)
    pwm_r = GPIO.PWM(ENB, 100)
    pwm_l.start(0)
    pwm_r.start(0)

def cleanup_hardware():
    pwm_l.stop()
    pwm_r.stop()
    GPIO.cleanup()