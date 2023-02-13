import buttonBindings as bindings
from XboxController import XboxController

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

import subprocess 

import time


keyboard = KeyboardController()
mouse = MouseController()

class ButtonFunctions:
  def __init__(self):
    pass
  
  def key_press(self, button):
    keyboard.press(button)
    keyboard.release(button)

  def mouse_press(self, button):
    mouse.press(button)
    mouse.release(button)

  def single_press(self, button):
    if type(button) == Key:
      self.key_press(button)
    elif type(button) == Button:
      self.mouse_press(button)
    else:
      subprocess.call(button, shell=True) 

      




if __name__ == '__main__':

  Xbox = XboxController()
  button_functions = ButtonFunctions()

  while 1:

    controller_values = Xbox.get_value()

    ##mouse movement
    move_x = controller_values['ABS_X']
    move_y = controller_values['ABS_Y']
    deadzone = 0.08
    if abs(move_x) < deadzone:
      move_x = 0
    if abs(move_y) < deadzone:
      move_y = 0
    if controller_values['BTN_THUMBL'] == 1:
      mouse.scroll(0, move_y * .7)
    else:
      mouse.move(pow(move_x * 2, 5), pow(move_y * -2, 5))

    ##joystick
    for key in bindings.button_binary_keys.keys():
      action = None

      if key in ['ABS_HAT0Y', 'ABS_HAT0X']:
        action = bindings.button_binary_keys[key][controller_values[key]]
      elif controller_values[key] > .02:
        action = bindings.button_binary_keys[key]

      if action != None:
          button_functions.single_press(action)
          time.sleep(0.08)


      


    time.sleep(0.001)
      