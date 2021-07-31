import serial
import msgpack
from pupper_hardware_interface import nonblocking_serial_reader
from pupper_hardware_interface import robot_state


class Interface:
    """Interface for reading from and controlling Pupper V2 robot.

    When you create an interface object it will 1) immediately connect to
    the robot, 2) set initial position control gains to normal
    values, and 3) set the max current to the safe value of 3.0 amps.

    Maybe in the future we will not send commands to the robot
    when you create this object for more safe / intuitive behavior.
    """
    def __init__(
        self,
        port,
        baudrate=500000,
        start_byte=0x00,
        initial_position_kp=14.0,
        initial_position_kd=2.0,
        initial_cartesian_kps=(5000.0, 5000.0, 3000.0),
        initial_cartesian_kds=(250.0, 250.0, 200.0),
        initial_max_current=2.0,
    ):
        self.start_byte = start_byte
        self.serial_handle = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0,
        )
        self.set_joint_space_parameters(
            initial_position_kp, initial_position_kd, initial_max_current
        )
        self.set_cartesian_parameters(
            initial_cartesian_kps, initial_cartesian_kds, initial_max_current
        )

        self.reader = nonblocking_serial_reader.NonBlockingSerialReader(
            self.serial_handle
        )

        self.robot_state = robot_state.RobotState()

    def read_incoming_data(self):
        decoded_data = None
        while True:
            data = self.reader.chew()
            if not data:
                return decoded_data
            try:
                decoded_data = msgpack.unpackb(data)
                self.robot_state.yaw = (
                    decoded_data["yaw"] if "yaw" in decoded_data else None
                )
                self.robot_state.pitch = (
                    decoded_data["pitch"] if "pitch" in decoded_data else None
                )
                self.robot_state.roll = (
                    decoded_data["roll"] if "roll" in decoded_data else None
                )
                self.robot_state.yaw_rate = (
                    decoded_data["yaw_rate"] if "yaw_rate" in decoded_data else None
                )
                self.robot_state.pitch_rate = (
                    decoded_data["pitch_rate"] if "pitch_rate" in decoded_data else None
                )
                self.robot_state.roll_rate = (
                    decoded_data["roll_rate"] if "roll_rate" in decoded_data else None
                )
                self.robot_state.position = (
                    decoded_data["pos"] if "pos" in decoded_data else None
                )
                self.robot_state.velocity = (
                    decoded_data["vel"] if "vel" in decoded_data else None
                )
                self.robot_state.current = (
                    decoded_data["cur"] if "cur" in decoded_data else None
                )
                self.robot_state.position_reference = (
                    decoded_data["pref"] if "pref" in decoded_data else None
                )
                self.robot_state.velocity_reference = (
                    decoded_data["vref"] if "vref" in decoded_data else None
                )
                self.robot_state.current_reference = (
                    decoded_data["cref"] if "cref" in decoded_data else None
                )
                self.robot_state.last_commanded_current = (
                    decoded_data["lcur"] if "lcur" in decoded_data else None
                )
            except ValueError as e:
                print(e)

    def send_dict(self, dict):
        payload = msgpack.packb(dict, use_single_float=True)
        start_sequence = bytes([self.start_byte, len(payload)])
        self.serial_handle.write(start_sequence + payload)

    def set_joint_space_parameters(self, kp, kd, max_current):
        self.send_dict({"kp": kp, "kd": kd, "max_current": max_current})

    def set_cartesian_parameters(self, kps, kds, max_current):
        """[summary]

        Parameters
        ----------
        kps : [list of size 3]
            kp gains, one for xyz
        kds : [list of size 3]
            kd gains, one for xyz
        max_current : [type]
            [description]
        """
        self.send_dict({"cart_kp": kps, "cart_kd": kds, "max_current": max_current})

    def activate(self):
        self.send_dict({"activations": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    def deactivate(self):
        self.send_dict(
            {"idle": True, "activations": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        )

    def zero_motors(self):
        self.send_dict({"zero": True})

    def home_motors(self):
        self.send_dict({"home": True})

    def set_actuator_postions(self, joint_angles):
        """[summary]

        Parameters
        ----------
        joint_angles : [numpy array (3, 4)]
            Joint angles, radians, with body axes RH rule convention
        """
        motor_frame_angles = joint_angles
        joint_angles_vector = motor_frame_angles.flatten("F").tolist()
        self.send_dict({"pos": joint_angles_vector})

    def set_cartesian_positions(self, cartesian_positions):
        """Sends desired cartesian positions to the Teensy

        Parameters
        ----------
        cartesian_positions : [numpy array (3, 4)]
            Desired cartesian positions of the feet [m], relative to the center of the body
        """
        cart_positions_list = cartesian_positions.flatten("F").tolist()
        self.send_dict({"cart_pos": cart_positions_list})
