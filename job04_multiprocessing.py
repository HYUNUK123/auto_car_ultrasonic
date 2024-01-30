from job01_hardware_setup import TRIG_r, ECHO_r, TRIG_m, ECHO_m, TRIG_l, ECHO_l
import job03_measure_distance as md
from multiprocessing import Process, Value, Array

def measure_process(trig_pin, echo_pin, target_list, index):
    while True:
        distance = md.measure_distance(trig_pin, echo_pin)
        target_list[index] = distance

def start_measure_multiprocessing(distances):
    process_r = Process(target=measure_process, args=(TRIG_r, ECHO_r, distances, 0))
    process_m = Process(target=measure_process, args=(TRIG_m, ECHO_m, distances, 1))
    process_l = Process(target=measure_process, args=(TRIG_l, ECHO_l, distances, 2))

    process_r.start()
    process_m.start()
    process_l.start()