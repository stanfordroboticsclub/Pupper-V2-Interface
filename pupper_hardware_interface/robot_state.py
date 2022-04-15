class RobotState(object):

    __slots__ = [
        "yaw",
        "pitch",
        "roll",
        "yaw_rate",
        "pitch_rate",
        "roll_rate",
        "position",
        "velocity",
        "current",
        "position_reference",
        "velocity_reference",
        "current_reference",
        "last_commanded_current",
        "mode",
    ]

    def __init__(
        self,
        yaw=None,
        pitch=None,
        roll=None,
        yaw_rate=None,
        pitch_rate=None,
        roll_rate=None,
        position=None,
        velocity=None,
        current=None,
        position_reference=None,
        velocity_reference=None,
        current_reference=None,
        last_commanded_current=None,
        mode=None,
    ):
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.yaw_rate = yaw_rate
        self.pitch_rate = pitch_rate
        self.roll_rate = roll_rate
        self.position = position
        self.velocity = velocity
        self.current = current
        self.position_reference = position_reference
        self.velocity_reference = velocity_reference
        self.current_reference = current_reference
        self.last_commanded_current = last_commanded_current
        self.mode = mode
