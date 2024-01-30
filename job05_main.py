import job01_hardware_setup as hs
import job02_mortor_control as mc
import job03_measure_distance as md
import job04_Threading as tc
import bluetooth_v2 as blue
import time
import threading

command = None

def bluetooth_listener(client_socket, server_socket):
    global command
    while True:
        command = blue.recv_string(client_socket, server_socket)

distances = [-1, -1, -1]
client_socket, server_socket = blue.setup_bluetooth()

bluetooth_thread = threading.Thread(target=bluetooth_listener, args=(client_socket, server_socket))
bluetooth_thread.start()

def control_car():
    hs.setup_hardware()
    tc.start_measure_multiprocessing(distances)
    while command == "1":
        if command != "1":
            break

        time.sleep(0.1)

        dist_r, dist_m, dist_l = md.measure_all_distances()

        if dist_r == -1 or dist_m == -1 or dist_l == -1:
            continue
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

        print("Right Speed:", RIGHT_SPEED, "Left speed:", LEFT_SPEED)
        print("---------------------------------------------------")
                        
    mc.stop()
    hs.cleanup_hardware()
try:
    while True:
        if command == "1":
            control_car()
        elif command == "0":
            print("car stop")
            pass
        elif command == "q":
            break
except KeyboardInterrupt:
    print("KeyboardInterrupt occurred!")

finally:
    client_socket.close()
    server_socket.close()
    print("Quit")
            

