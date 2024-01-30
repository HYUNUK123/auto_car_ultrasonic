import job01_hardware_setup
from job01_hardware_setup import TRIG_r, ECHO_r, TRIG_m, ECHO_m, TRIG_l, ECHO_l
import RPi.GPIO as GPIO
import time


def measure_distance(trig_pin, echo_pin, num_measurements=5):
    for _ in range(num_measurements):


        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        time.sleep(0.3)
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)

        pulse_start = time.time()
        pulse_end = time.time()

        timeout = time.time()
        while GPIO.input(echo_pin) == 0 and time.time() - timeout < 0.1:
            pulse_start = time.time()

        timeout = time.time()
        while GPIO.input(echo_pin) == 1 and time.time() - timeout < 0.1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        if 5 <= distance <= 250:  # 첫 번째 유효한 거리 측정값 반환
            return distance

    return 1  # 유효한 측정값이 없을 경우 -1 반환


def measure_all_distances():
    dist_r = measure_distance(TRIG_r, ECHO_r)
    dist_m = measure_distance(TRIG_m, ECHO_m)
    dist_l = measure_distance(TRIG_l, ECHO_l)
    return dist_r, dist_m, dist_l