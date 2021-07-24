class RobotState(object):

    __slots__ = [
        "position",
        "velocity",
        "current",
        "position_reference",
        "velocity_reference",
        "current_reference",
        "last_commanded_current",
    ]

    def __init__(
        self,
        position=None,
        velocity=None,
        current=None,
        position_reference=None,
        velocity_reference=None,
        current_reference=None,
        last_commanded_current=None,
    ):
        self.position = position
        self.velocity = velocity
        self.current = current
        self.position_reference = position_reference
        self.velocity_reference = velocity_reference
        self.current_reference = current_reference
        self.last_commanded_current = last_commanded_current
