import buttonBindings as binding
from inputs import get_gamepad

from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as MouseController

keyboard = Controller()
mouse = MouseController()

import time



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

      




if __name__ == '__main__':

  button = ButtonFunctions()

  while 1:

    events = get_gamepad() #notable behavior, code stop on this line until an event is received

    for event in events:                                                      #event loop start

      for key in binding.button_binary_keys.keys():                           #single_press_key loop start
        if event.code == key:
          action = None
          if key == 'ABS_HAT0Y' or key == 'ABS_HAT0X':
            action = binding.button_binary_keys[event.code][event.state]
          else:
            if event.state == 1:
              action = binding.button_binary_keys[key]
          print(action)
          if action != None:
            button.single_press(action)
          
      
    time.sleep(0.01)
      