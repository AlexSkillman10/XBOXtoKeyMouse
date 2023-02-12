from pynput.keyboard import Key,Controller
keyboard = Controller()


class PCfunctions:
  def __init__(self):
    pass

  def volumeUp():
    keyboard.press(Key.media_volume_up)
    keyboard.release(Key.media_volume_up)

  def volumeDown():
    keyboard.press(Key.media_volume_down)
    keyboard.release(Key.media_volume_down)

  def volumeMute():
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)
  
  def mediaPlay():
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)
  
  def mediaNext():
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)
  
  def mediaPrevious():
    keyboard.press(Key.media_previous)
    keyboard.release(Key.media_previous)

  
