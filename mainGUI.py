import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


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



class App(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry('800x400')
        self.title('Xbox Controller GUI')

        self.set_theme("equilux")

  
        # Configure the dark theme colors
        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="#222222")
        self.style.configure("TLabel", background="#222222", foreground="white")

        self.configure(bg=self.style.lookup('TFrame', 'background'))

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        # label
        self.controller_status = tk.StringVar()
        self.controller_status.set("Controller Status: Unknown")

        label_font = ("Helvetica", 14, "bold")

        style = ttk.Style()
        style.configure("RedText.TLabel", foreground="white", font=label_font, background="#222222")

        self.status_label = ttk.Label(self.main_frame, textvariable=self.controller_status, style="RedText.TLabel")
        self.status_label.grid(column=0, row=0, padx=5, pady=5, sticky='w')

         # Letter list frame
        self.letters_frame = ttk.Frame(self.main_frame)
        self.letters_frame.grid(column=0, row=1, padx=10, pady=70, sticky='nsew')

        # Image frame
        self.image_frame = ttk.Frame(self.main_frame)
        self.image_frame.grid(column=1, row=1, padx=10, pady=10, sticky='nsew')

        # Create alphabet list
        self.alphabet_list = tk.Listbox(self.letters_frame, font=("Helvetica", 14), bg="#222222", fg="white", selectbackground="#4a4a4a")
        self.alphabet_list.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.alphabet_list.insert(tk.END, letter)


        img = Image.open("xbox_controller.PNG")
        image_scaler = 0.4

        # Create a Canvas widget to display the images
        self.canvas = tk.Canvas(self.image_frame, width=int(img.size[0]*image_scaler), height=int(img.size[1]*image_scaler), bg="#222222", bd=0, highlightthickness=0)
        self.canvas.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        # Xbox controller image
        img_resized = img.resize((int(img.size[0]*image_scaler), int(img.size[1]*image_scaler)), Image.ANTIALIAS)
        self.xbox_controller_img = ImageTk.PhotoImage(img_resized)
        self.canvas.create_image(0, 0, image=self.xbox_controller_img, anchor='nw')

        self.overlay_images = {}
        for button in ['a', 'b', 'x', 'y', 'blank']:
            overlay_img = Image.open(f"button_hovers/{button}.PNG")
            overlay_img_resized = overlay_img.resize((int(img.size[0]*image_scaler), int(img.size[1]*image_scaler)), Image.ANTIALIAS)
            self.overlay_images[button] = ImageTk.PhotoImage(overlay_img_resized)

        # Define the bounding boxes for the buttons (replace these values with the actual coordinates)
        self.button_coordinates = {
            'a': (323, 128, 358, 160),
            'y': (323, 70, 358, 104),
            
        }

        self.overlay_id = self.canvas.create_image(0, 0, image=None, anchor='nw')

        self.canvas.bind('<Motion>', self.on_mouse_hover)

        self.xbox_controller = XboxController()
        self.update_status()

    def on_mouse_hover(self, event):
        x, y = event.x, event.y

        print(f"Current mouse position: ({x}, {y})")

        for button, (x1, y1, x2, y2) in self.button_coordinates.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.canvas.itemconfig(self.overlay_id, image=self.overlay_images[button])
                break
        else:
            self.canvas.itemconfig(self.overlay_id, image=self.overlay_images['blank'])

    def update_status(self):
        if self.xbox_controller.controller_status:
            self.controller_status.set("Controller Status: Connected")
        else:
            self.controller_status.set("Controller Status: Disconnected")
        self.after(100, self.update_status)

if __name__ == "__main__":
    app = App()
    app.mainloop()






      
        