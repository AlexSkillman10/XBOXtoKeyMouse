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


class MainApp(ThemedTk):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    #get objects
    self.xbox_controller = XboxController()
    self.current_macro = Macro()

    #basic setup
    self.title('Xbox Controller GUI')
    self.geometry('900x600')
    self.set_theme("equilux")

    #review this section 
    self.style = ttk.Style(self)
    self.style.configure("TFrame", background="#222222")
    self.style.configure("TLabel", background="#222222", foreground="white")
    self.configure(bg=self.style.lookup('TFrame', 'background'))
    self.style.configure("Custom.TEntry", fieldbackground=self.style.lookup('TFrame', 'background'), foreground="white", background=self.style.lookup('TFrame', 'background'))
    self.style.configure("Custom.TButton", fieldbackground=self.style.lookup('TFrame', 'background'), foreground="white", background=self.style.lookup('TFrame', 'background'), font=("Trebuchet MS", 10), anchor='center')

    #create frames

    #main frame
      #col |1 : changes size to center col 2
      #col |2
        #col |2|1 : contains the xbox section
          #row |2|1-1 : contains the xbox entry frame
          #row |2|1-2 : contains the xbox image frame
        #col |2|2 : contains the pc section
          #row |2|2-1 : contains the pc entry frame
          #row |2|2-2 : contains the pc listbox
      #col |3

    #main frame  
    self.main_frame = ttk.Frame(self)
    self.main_frame.pack(fill=tk.BOTH, expand=True)

      #col |1 : changes size to center col 2
    self.centering_column = ttk.Frame(self.main_frame)
    self.centering_column.grid(row=0, column=0, padx = 0, sticky="nsew")
    self.bind('<Configure>', self.update_centering_pad)

      #col |2
    self.centered_column = ttk.Frame(self.main_frame)
    self.centered_column.grid(row=0, column=1, sticky="nsew")

        #col |2|1 : contains the xbox section
    self.xbox_frame = ttk.Frame(self.centered_column)
    self.xbox_frame.grid(row=0, column=0, sticky="nsew")

          #row |2|1-1 : contains the xbox entry frame
    self.xbox_entry_frame = ttk.Frame(self.xbox_frame)
    self.xbox_entry_frame.grid(column=0, row=0, padx=(0, 0), pady=0, sticky='n')

    self.xbox_label = ttk.Label(self.xbox_entry_frame, text="XBOX", font=("Trebuchet MS", 25, "bold"))
    self.xbox_label.grid(column=0, row=0, padx=0, pady=(10, 0), sticky='nsew')

    self.xbox_trash_button = ttk.Button(self.xbox_entry_frame, text="🗑️", command=None, style="Custom.TButton", width=3)
    self.xbox_trash_button.grid(column=0, row=0, padx=0, pady=(0, 0), sticky='se')

    self.xbox_entry_label = tk.StringVar()
    self.xbox_entry = ttk.Entry(self.xbox_entry_frame, textvariable=self.xbox_entry_label, width=34, font=("Trebuchet MS", 13), style="Custom.TEntry", state='readonly', cursor='arrow')
    self.xbox_entry.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')

          #row |2|1-2 : contains the xbox image frame
    self.image_frame = ttk.Frame(self.xbox_frame)
    self.image_frame.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')

    img = Image.open("xbox_controller_on.PNG")
    image_scaler = 0.4

    self.canvas = tk.Canvas(self.image_frame, width=int(img.size[0]*image_scaler), height=int(img.size[1]*image_scaler), bg="#222222", bd=0, highlightthickness=0)
    self.canvas.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')

    self.base_id = self.canvas.create_image(0, 0, image=None, anchor='nw')
    self.base_images = {}
    for button in ['on', 'off']:
        base_img = Image.open(f"xbox_controller_{button}.PNG")
        base_img_resized = base_img.resize((int(img.size[0]*image_scaler), int(img.size[1]*image_scaler)), Image.ANTIALIAS)
        self.base_images[button] = ImageTk.PhotoImage(base_img_resized)
    self.update_status()

    self.overlay_id = self.canvas.create_image(0, 0, image=None, anchor='nw')
    self.overlay_images = {}
    for button in ['a', 'b', 'x', 'y', 'blank', 'sel', 'start', 'd_up', 'd_down', 'd_right', 'd_left']:
        overlay_img = Image.open(f"button_hovers/{button}.PNG")
        overlay_img_resized = overlay_img.resize((int(img.size[0]*image_scaler), int(img.size[1]*image_scaler)), Image.ANTIALIAS)
        self.overlay_images[button] = ImageTk.PhotoImage(overlay_img_resized)
    self.button_coordinates = {
        'a': (323, 128, 358, 160),
        'y': (323, 70, 358, 104),

        'x': (295, 100, 328, 133),
        'b': (355, 100, 388, 133),

        'sel': (252, 105, 273, 126),
        'start': (190, 105, 211, 126),

        'd_up': (166, 150, 188, 175),
        'd_down': (166, 190, 188, 220),

        'd_left': (144, 170, 168, 194),
        'd_right': (188, 170, 208, 194),
      }
    self.canvas.bind('<Motion>', self.on_mouse_hover)

    self.canvas.bind('<Button-1>', self.on_canvas_click)

        #col |2|2 : contains the pc section
    self.pc_frame = ttk.Frame(self.centered_column)
    self.pc_frame.grid(column=1, row=0, sticky="nsew")

          #row |2|2-1 : contains the pc entry frame
    self.pc_entry_frame = ttk.Frame(self.pc_frame)
    self.pc_entry_frame.grid(column=0, row=0, padx=(0, 0), pady=0, sticky='n')

    self.pc_label = ttk.Label(self.pc_entry_frame, text="PC", font=("Trebuchet MS", 25, "bold"))
    self.pc_label.grid(column=0, row=0, padx=0, pady=(10, 0), sticky='nsew')

    self.pc_trash_button = ttk.Button(self.pc_entry_frame, text="🗑️", command=None, style="Custom.TButton", width=3)
    self.pc_trash_button.grid(column=0, row=0, padx=0, pady=(0, 0), sticky='se')

    self.pc_entry_label = tk.StringVar()
    self.pc_entry = ttk.Entry(self.pc_entry_frame, textvariable=self.pc_entry_label, width=34, font=("Trebuchet MS", 13), style="Custom.TEntry", state='readonly', cursor='arrow')
    self.pc_entry.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')

          #row |2|2-2 : contains the pc listbox


    self.update_idletasks()
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

  def update_centering_pad(self, event=None):
    self.update_idletasks() 
    window_width = self.winfo_width()
    centered_column_width = self.centered_column.winfo_width()

    difference = window_width - centered_column_width
    if difference > 0:
      padx = difference // 2
      self.centered_column.grid_configure(padx=padx)

  def update_status(self):
    if self.xbox_controller.controller_status:
        self.canvas.itemconfig(self.base_id, image=self.base_images['on'])
    else:
        self.canvas.itemconfig(self.base_id, image=self.base_images['off'])
    self.after(100, self.update_status)

  def on_canvas_click(self, event):
    x, y = event.x, event.y
    for button, (x1, y1, x2, y2) in self.button_coordinates.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            if button.upper() not in self.current_macro.xbox_binds:
                self.current_macro.add_bind(button.upper())
            xbox_bind_string =""
            for bind in self.current_macro.xbox_binds:
                xbox_bind_string += f"{bind}+"
            if xbox_bind_string[-1] == "+":
                xbox_bind_string = xbox_bind_string[:-1]
            self.xbox_entry_label.set(xbox_bind_string)



        






class Macro():
    def __init__(self):
        self.xbox_binds = []
        self.pc_binds = []
        self.sequence = False
    
    def add_bind(self, xbox_bind):
        self.xbox_binds.append(xbox_bind)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()