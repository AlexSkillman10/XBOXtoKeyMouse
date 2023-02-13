import buttonBindings as bindings
from XboxController import XboxController

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

import pydirectinput


import time




keyboard = KeyboardController()
mouse = MouseController()

class ButtonFunctions:
  def __init__(self):
    self.left_mouse_state = 0
  
  def key_press(self, button):
    keyboard.press(button)
    keyboard.release(button)

  def change_mouse_left_state(self, value):
    if self.left_mouse_state != value:
        self.left_mouse_state = value
        if value == 1:
          pydirectinput.mouseDown()
        else:
          pydirectinput.mouseUp()

  def mouse_press(self, button):
      mouse.press(button)
      mouse.release(button)

  def single_press(self, button):
    if type(button) == Button:
      self.mouse_press(button)
    else:
      self.key_press(button)


if __name__ == '__main__':

  Xbox = XboxController()
  button_functions = ButtonFunctions()

  button_update_cycle = 13
  button_update_counter = 0

  enable_function = True
  while 1:
    
    controller_values = Xbox.get_value()
    ##mouse movement
    move_x = controller_values['ABS_X']
    move_y = controller_values['ABS_Y']
    deadzone = bindings.joystick_deadzone

    if abs(move_x) < deadzone:
      move_x = 0
    if abs(move_y) < deadzone:
      move_y = 0

    if controller_values['BTN_THUMBL'] == 1:
      mouse.scroll(0, move_y * .4)
    else:
      base_sens = bindings.joystick_sensitivity_base_multiplier
      sens_curve = bindings.joystick_applied_power_curve
      mouse.move(pow(move_x * base_sens, sens_curve), pow(move_y * -base_sens, sens_curve))

    ##binary_buttons
    if button_update_counter >= button_update_cycle:
      for key in bindings.button_binary_keys.keys():

        action = bindings.button_binary_keys[key]

        if key in ['ABS_HAT0Y', 'ABS_HAT0X']:
          action = action[controller_values[key]]

        if action == Button.left:
          button_functions.change_mouse_left_state(controller_values[key])
        elif action != None and abs(controller_values[key]) > .02:
            button_functions.single_press(action)
            button_update_counter=0
    
    button_update_counter += 1
    time.sleep(0.01)
      