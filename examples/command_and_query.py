from pupper_hardware_interface import interface
import time
import numpy as np
import argparse
from serial.tools import list_ports

print("WARNING: ONLY TESTED ON MACOS 11.4.")

# Try to get the name of the Teensy serial port by
# finding the first serial device with 'usbmodem' in its name
usbmodem = next(list_ports.grep(".*usbmodem.*")).device
parser = argparse.ArgumentParser(description="Command and query Pupper V2")
parser.add_argument(
    "--serial_port",
    default=usbmodem,
    action="store",
    type=str,
    help='Path to the Teensy serial port e.g. "/dev/tty.usbmodem73090601". Defaults to first serial port containing the phrase "usbmodem"',
)
args = parser.parse_args()

# Connect to Pupper V2
print("Connecting to ", args.serial_port, "...")
pupperv2 = interface.Interface(args.serial_port)
time.sleep(0.25)
print("Connected.")
input("Press enter to actuate the motors and read telemetry.")

# Set to kp=14, kd=2, max_current=7.0 (or 10.0) for higher performance
pupperv2.set_joint_space_parameters(kp=3.0, kd=1.0, max_current=2.0)

last_print = time.time()
try:
    while True:
        pupperv2.read_incoming_data()
        print("Base orientation (YPR): ", pupperv2.robot_state.yaw, pupperv2.robot_state.pitch, pupperv2.robot_state.roll)
        print("Base angular velocity: ", pupperv2.robot_state.yaw_rate, pupperv2.robot_state.pitch_rate, pupperv2.robot_state.roll_rate)
        print("Actuator positions: ", pupperv2.robot_state.position)
        print("Actuator velocities: ", pupperv2.robot_state.velocity)

        #
        pupperv2.set_actuator_postions(np.zeros((3, 4)))

        # Sleep long enough so that the loop runs at about 200Hz
        time.sleep(0.003)
        end = time.time()
        print("Loop rate: ", 1.0 / (end - last_print))
        last_print = end
except KeyboardInterrupt:
    print("exiting")
