from inputs import get_gamepad
import inputs
import threading
import time

class XboxController(object):


    def __init__(self):
        self.controller_values = {
            'ABS_Y': 0,
            'ABS_X': 0,
            'ABS_RY': 0,
            'ABS_RX': 0,
            'ABS_Z': 0,
            'ABS_RZ': 0,
            'BTN_TR': 0,
            'BTN_TL': 0,
            'BTN_WEST': 0,
            'BTN_NORTH': 0,
            'BTN_SOUTH': 0,
            'BTN_EAST': 0,
            'BTN_THUMBR': 0,
            'BTN_THUMBL': 0,
            'BTN_SELECT': 0,
            'BTN_START': 0,
            'ABS_HAT0Y': 0,
            'ABS_HAT0X': 0,
        }

        self.controller_status = None

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def get_value(self):
        return self.controller_values

    def change_plug_state(self, state):
        if self.controller_status != state:
            self.controller_status = state
            print("Controller Status: ", state)


    def _monitor_controller(self):
        while True:
            events = []
            try:
                events = get_gamepad()
                self.change_plug_state('Connected')
            except inputs.UnpluggedError:
                self.change_plug_state('Disconnected')
                inputs.devices._detect_gamepads()
                time.sleep(.5)
            
            for event in events:
                for key in self.controller_values.keys():
                    if event.code == key and event.code in ['ABS_Y', 'ABS_X', 'ABS_RY', 'ABS_RX']:
                        self.controller_values[key] = event.state / 32768
                    elif event.code == key and event.code in ['ABS_Z', 'ABS_RZ']:
                        self.controller_values[key] = event.state / 256
                    elif event.code == key:
                        self.controller_values[key] = event.state