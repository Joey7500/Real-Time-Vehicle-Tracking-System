# Placeholder for optional serial trigger (e.g., beam sensor).
class ArduinoTrigger:
    def __init__(self, port="/dev/ttyACM0", baud=115200):
        self.port = port; self.baud = baud
    def read_event(self):
        return None  # TODO: implement serial read
