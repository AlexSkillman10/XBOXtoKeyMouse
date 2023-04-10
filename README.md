# Summary
This script is intended to allow you to move your mouse, type, play/pause, 
change volume, start programs, among other things, all with the use of an XBOX controller.

You can change the bindings to your liking in buttonBindings, as well as other settings.

The original idea with this was to create something I could use as a TV remote,
since the TV in my dorm was connected to my PC. I hope you can find other uses.
If you have any issues or feature ideas, raise an issue on github or email me at
alexskillman10@gmail.com

# Installation and Usage

This program runs using three python packages: pynput, inputs, and pydirectinput.
You can enter the following commands with bash or the terminal to install them

>pip install inputs

>pip install pynput

>pip install pydirectinput

After these have installed, run main.py with python 2.9 or newer.
If your controller is connected, try moving a stick or pressing a button.
The controller status should appear in the window.

# Known Issues
In all Windows' menus, you will notice the controller will move selection up and down
when you attempt to move the mouse, or use the d-pad. Unfortunately, Microsoft provides no reliable
way to disable this 'feature,' even using the registry editor. You can get around this by pausing the program
by pressing the two stick buttons at the same time, and pressing them again when you are done.

# Changing settings

You can change the bindings of the remote by modifying the variables in buttonBindings.py.
Check out the links for specific keys. If you want to link it to just a character,
simply type 'a', or 'x' (must be single character). To link a button to a program,
link the path as a string to the the button in bindings.py. You will most likely
need ot change all the backslashes into forward slashes

# Default Controls

