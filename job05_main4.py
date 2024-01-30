import job01_hardware_setup as hs
import job02_mortor_control as mc
import job03_measure_distance as md
import job04_multiprocessing as tp
import bluetooth_v2 as blue
import time
import threading
import logging

start_time = time.time()
prev_message_time = start_time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_with_time(level, message):
    global prev_message_time
    current_time = time.time()

    time_since_start = current_time - start_time
    time_since_last_message = current_time - prev_message_time

    formatted_message = f"{message} (after {time_since_last_message:.4f} sec)"
    if level == 'DEBUG':
        logging.debug(formatted_message)
    elif level == 'INFO':
        logging.info(formatted_message)

    prev_message_time = current_time



command = None

def bluetooth_listener(client_socket, server_socket):
    global command
    while True:
        command = blue.recv_string(client_socket, server_socket)

distances = [-1, -1, -1]
client_socket, server_socket = blue.setup_bluetooth()

bluetooth_thread = threading.Thread(target=bluetooth_listener, args=(client_socket, server_socket))
bluetooth_thread.start()

pre_dist_r = 0.0
pre_dist_m = 0.0
pre_dist_l = 0.0
ROTATION = 40
STRAIT_SPEED = 30

def control_car():
    global pre_dist_r, pre_dist_m, pre_dist_l
    log_with_time('INFO', "start")
    hs.setup_hardware()
    log_with_time('INFO', "setup")
    while command == "1":
        if command != "1":
            break

        time.sleep(0.1)

        dist_r, dist_m, dist_l = md.measure_all_distances()
        log_with_time('INFO', "measure_distances")
        if dist_r != -1:
            pre_dist_r = dist_r
        elif dist_r == -1:
            dist_r = pre_dist_r

        if dist_m != -1:
            pre_dist_m = dist_m
        elif dist_m == -1:
            dist_m = pre_dist_m

        if dist_l != -1:
            pre_dist_l = dist_l
        elif dist_l == -1:
            dist_l = pre_dist_l

        print("Right Distance:", dist_r, "cm", "Middle Distance:", dist_m, "cm", "Left Distance:", dist_l,
                  "cm")

        DEFAULT_SPEED = 50
        RIGHT_SPEED = 50
        LEFT_SPEED = 50

        if dist_l >= dist_r:
            long_wave = dist_l
            short_wave = dist_r
        else:
            long_wave = dist_r
            short_wave = dist_l

        distance_rate = long_wave / short_wave

        if dist_l >= dist_r:
            LEFT_SPEED = LEFT_SPEED * (1 / distance_rate)
            RIGHT_SPEED = DEFAULT_SPEED
        else:
            RIGHT_SPEED = RIGHT_SPEED * (1 / distance_rate)
            LEFT_SPEED = DEFAULT_SPEED

        mc.forward_l(LEFT_SPEED)
        mc.forward_r(RIGHT_SPEED)
        log_with_time('INFO', "move")

        print("---------------------------------------------------")

    mc.stop()
    hs.cleanup_hardware()
try:
    while True:
        if command == "1":
            control_car()
        elif command == "0":
            hs.setup_hardware()
            dist_r, dist_m, dist_l = md.measure_all_distances()
            print("Right Distance:", dist_r, "cm", "Middle Distance:", dist_m, "cm", "Left Distance:", dist_l,
                    "cm")
            log_with_time('INFO', "measure_distances")
            hs.cleanup_hardware()

            pass
        elif command == "q":
            break
except KeyboardInterrupt:
    print("KeyboardInterrupt occurred!")

finally:
    client_socket.close()
    server_socket.close()
    print("Quit")
            
