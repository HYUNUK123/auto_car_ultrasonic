import job01_hardware_setup
from job01_hardware_setup import TRIG_r, ECHO_r, TRIG_m, ECHO_m, TRIG_l, ECHO_l
import RPi.GPIO as GPIO
import time
import numpy as np

def measure_distance(trig_pin, echo_pin, num_measurements=5):
    measurements = []
    for _ in range(num_measurements):
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(trig_pin, False)
        time.sleep(0.01)

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

        if 5 <= distance <= 300:  # 첫 번째 유효한 거리 측정값 반환
            measurements.append(distance)

            # 이상치 제거 및 메디안 필터 적용
            if len(measurements) > 0:
                measurements.sort()
                # 중간값 반환
                median_distance = np.median(measurements)
                return median_distance


def measure_all_distances():
    dist_r = measure_distance(TRIG_r, ECHO_r)
    dist_m = measure_distance(TRIG_m, ECHO_m)
    dist_l = measure_distance(TRIG_l, ECHO_l)
    return dist_r, dist_m, dist_l