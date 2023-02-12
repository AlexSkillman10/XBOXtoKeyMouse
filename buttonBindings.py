#use this file to set your preffered button bindings. 
#you can find a list of keys here:
#https://pynput.readthedocs.io/en/latest/keyboard.html
from pynput.keyboard import Key
from pynput.mouse import Button

#buttons
right_bumper = Key.media_volume_up
left_bumper = None

#triggers buttons
left_trigger = None
right_trigger = None

#circle buttons
x_button = None
y_button = None
a_button = Button.left
b_button = None

#d-pad buttons
d_pad_up = Key.media_volume_up
d_pad_down = Key.media_volume_down
d_pad_left = Key.media_volume_mute
d_pad_right = Key.media_play_pause


##button links to input codes. DO NOT MODIFY
button_binary_keys = {
  'BTN_TR': right_bumper, 
  'BTN_TL': left_bumper,

  'BTN_WEST': x_button,
  'BTN_NORTH': y_button,
  'BTN_SOUTH': a_button,
  'BTN_EAST': b_button,

  'ABS_HAT0Y': [None, d_pad_down, d_pad_up],
  'ABS_HAT0X': [None, d_pad_right, d_pad_left],
  }








