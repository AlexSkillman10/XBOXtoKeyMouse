from pynput.keyboard import Key
from pynput.mouse import Button

# use this file to set your preffered button bindings. Analog stick functions cannot be changed,
# but you can change the deadzones and mouse movement sensitivity

# you can find a list of keys here:
# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://pynput.readthedocs.io/en/latest/mouse.html


#bumper bindings
right_bumper = None
left_bumper = None

#trigger bindings
left_trigger = None
right_trigger = None

#circle button bindings
x_button = Key.backspace 
y_button = None
a_button = Button.left
b_button = Button.right

#d-pad bindings
d_pad_up = Key.media_volume_up
d_pad_down = Key.media_volume_down
d_pad_left = Key.media_volume_mute
d_pad_right = Key.media_play_pause

#center button select/start bindings
select_button = None
start_button = None

#joystick button bindings
right_joystick = None
left_joystick = None #currently used to scroll with left joystick. Do not change

#joystick deadzone
joystick_deadzone = 0.08
joystick_sensitivity_base_multiplier = 2 #Changes base sensitivity of joystick.
joystick_applied_power_curve = 5 #do not recommend changing, if you do IT MUST BE ODD. Changes the sensitivity curve.



##button links to input codes. DO NOT MODIFY
button_binary_keys = {
  'BTN_TR': right_bumper, 
  'BTN_TL': left_bumper,

  'BTN_WEST': x_button,
  'BTN_NORTH': y_button,
  'BTN_SOUTH': a_button,
  'BTN_EAST': b_button,

  'ABS_Z': left_trigger,
  'ABS_RZ': right_trigger,  

  'BTN_THUMBR': right_joystick,
  'BTN_THUMBL': left_joystick,

  'BTN_SELECT': select_button,
  'BTN_START': start_button,

  'ABS_HAT0Y': [None, d_pad_down, d_pad_up],
  'ABS_HAT0X': [None, d_pad_right, d_pad_left],
  }








