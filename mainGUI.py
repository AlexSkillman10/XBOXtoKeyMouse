import tkinter as tk
from tkinter import ttk

import os
import sys

import buttonBindings as bindings
from XboxController import XboxController

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

from pystray import MenuItem as item

import time

from pystray import MenuItem as item
import pystray

from PIL import Image, ImageTk



import os
import sys

import buttonBindings as bindings
from XboxController import XboxController

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

from pystray import MenuItem as item

import time

from pystray import MenuItem as item
import pystray

from PIL import Image, ImageTk



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Xbox Controller Interface")
        self.configure(bg='black')  # Set background to black
        self.geometry("300x200")

        self.frame = tk.Frame(self, bg='black')
        self.frame.pack(padx=10, pady=10)

        self.wm_iconbitmap('xbox.ico')


        self.controller_status = tk.StringVar()
        self.controller_status.set("Controller Status: Unknown")
        self.status_label = tk.Label(self.frame, textvariable=self.controller_status)
        self.status_label.grid(row=0, column=0, columnspan=2)

        self.protocol('WM_DELETE_WINDOW', self.hide_window)

        self.xbox_controller = XboxController()
        self.update_status()

        self.update()
        self.frame.config(highlightbackground='teal', highlightthickness=1)

        self.icon = None

        # Custom buttons
        self.button_frame = tk.Frame(self, bg='black')
        self.button_frame.pack(side=tk.TOP, anchor=tk.E)

      
    def quit_window(self):
        self.icon.stop()
        self.destroy()

    def show_window(self):
        self.icon.stop()
        self.deiconify()

    def update_status(self):
        if self.xbox_controller.controller_status:
            self.controller_status.set("Controller Status: Connected")
        else:
            self.controller_status.set("Controller Status: Disconnected")
        self.after(100, self.update_status)

    def hide_window(self):
        self.withdraw()
        image = Image.open("xbox.ico")
        menu = (item('Show', self.show_window), item('Quit', self.quit_window))
        self.icon = pystray.Icon("name", image, "My System Tray Icon", menu)
        self.icon.run()


if __name__ == '__main__':
    app = App()
    app.mainloop()






      
        