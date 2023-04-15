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

class App(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xbox_controller = XboxController()
        self.current_macro = Macro()


        self.title('Xbox Controller GUI')
        self.geometry('900x600')
        self.set_theme("equilux")

        # Configure the dark theme colors
        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="#222222")
        self.style.configure("TLabel", background="#222222", foreground="white")
        self.configure(bg=self.style.lookup('TFrame', 'background'))
        self.style.configure("Custom.TEntry", fieldbackground=self.style.lookup('TFrame', 'background'), foreground="white", background=self.style.lookup('TFrame', 'background'))
        self.style.configure("Custom.TButton", fieldbackground=self.style.lookup('TFrame', 'background'), foreground="white", background=self.style.lookup('TFrame', 'background'), font=("Trebuchet MS", 10), anchor='center')
        



        # Main frame ======================================================================================================================================\/ \/ \/
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')

        # Top Row ================================================================================================================================\/ \/ \/
        self.top_row = ttk.Frame(self.main_frame)
        self.top_row.grid(column=0, row=1, padx=0, pady=23, sticky='nsew')

        # Centering Pad=================================================================================================================\/ \/ \/
        self.centering_pad = ttk.Frame(self.top_row)
        self.centering_pad.grid(column=0, row=0, padx=0, pady=0, sticky='nsew') 
        # Centering Pad=================================================================================================================/\ /\ /\

        # Image frame ==================================================================================================================\/ \/ \/
        self.image_frame = ttk.Frame(self.top_row)
        self.image_frame.grid(column=1, row=0, padx=(0, 30), pady=0, sticky='nsew')  # Change row from 0 to 1

        img = Image.open("xbox_controller_on.PNG")
        image_scaler = 0.4

        # Image canvas ==============================================================================\/ \/ \/
        self.canvas = tk.Canvas(self.image_frame, width=int(img.size[0]*image_scaler), height=int(img.size[1]*image_scaler), bg="#222222", bd=0, highlightthickness=0)
        self.canvas.grid(column=0, row=0, padx=0, pady=7, sticky='nsew')

        self.base_images = {}
        for button in ['on', 'off']:
            base_img = Image.open(f"xbox_controller_{button}.PNG")
            base_img_resized = base_img.resize((int(img.size[0]*image_scaler), int(img.size[1]*image_scaler)), Image.ANTIALIAS)
            self.base_images[button] = ImageTk.PhotoImage(base_img_resized)

        self.overlay_images = {}
        for button in ['a', 'b', 'x', 'y', 'blank', 'sel', 'start', 'd_up', 'd_down', 'd_right', 'd_left']:
            overlay_img = Image.open(f"button_hovers/{button}.PNG")
            overlay_img_resized = overlay_img.resize((int(img.size[0]*image_scaler), int(img.size[1]*image_scaler)), Image.ANTIALIAS)
            self.overlay_images[button] = ImageTk.PhotoImage(overlay_img_resized)

        # Define the bounding boxes for the buttons (replace these values with the actual coordinates)
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

        self.base_id = self.canvas.create_image(0, 0, image=None, anchor='nw')
        self.overlay_id = self.canvas.create_image(0, 0, image=None, anchor='nw')
        self.canvas.bind('<Motion>', self.on_mouse_hover)
        # Image canvas ==============================================================================/\ /\ /\
        # Image frame ==================================================================================================================/\ /\ /\

        # Binds frame ==================================================================================================================\/ \/ \/
        self.binds_frame = ttk.Frame(self.top_row)
        self.binds_frame.grid(column=2, row=0, padx=0, pady=0, sticky='nsew')
        self.listbox = tk.Listbox(self.binds_frame, width=40, height=20, bg="#222222", fg="white", selectbackground="#222222", selectforeground="white")
        self.listbox.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.listbox.insert(1, "A")
        self.listbox.insert(2, "B")
        self.listbox.insert(3, "X")
        self.listbox.insert(4, "Y")
        self.listbox.insert(5, "Start")
        # Binds frame ==================================================================================================================/\ /\ /\
        # Top Row ================================================================================================================================/\ /\ /\

        # Mid Row ================================================================================================================================\/ \/ \/
        self.mid_row = ttk.Frame(self.main_frame)
        self.mid_row.grid(column=0, row=0, padx=0, pady=20, sticky='nsew')

        # Centering Pad=================================================================================================================\/ \/ \/
        self.centering_pad2 = ttk.Frame(self.mid_row)
        self.centering_pad2.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        # Centering Pad=================================================================================================================/\ /\ /\

        # Set Bind Frame ===============================================================================================================\/ \/ \/
        self.set_frame = ttk.Frame(self.mid_row)
        self.set_frame.grid(column=1, row=0, padx=0, pady=0, sticky='nsew')

        # Add the two Entry widgets and the arrow label
        # Set Entry Frame =====================================================================================================\/ \/ \/
        self.set_entry_frame = ttk.Frame(self.set_frame)
        self.set_entry_frame.grid(column=0, row=0, padx=(0, 20), pady=0, sticky='nsew')

        self.arrow_label = ttk.Label(self.set_entry_frame, text="XBOX", font=("Trebuchet MS", 25, "bold"))
        self.arrow_label.grid(column=0, row=0, padx=0, pady=(10, 0), sticky='nsew')

        # create trash button to reset string
        self.trash_button = ttk.Button(self.set_entry_frame, text="🗑️", command=self.reset_button_name_var, style="Custom.TButton", width=3)
        self.trash_button.grid(column=0, row=0, padx=0, pady=(0, 0), sticky='se')

        self.button_name_var = tk.StringVar()
        self.entry1 = ttk.Entry(self.set_entry_frame, textvariable=self.button_name_var, width=34, font=("Trebuchet MS", 13), style="Custom.TEntry", state='readonly', cursor='arrow')
        self.entry1.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')
        # Set Entry Frame =====================================================================================================/\ /\ /\

        # Center Arrow ========================================================================================================\/ \/ \/

        self.set_entry_frame3 = ttk.Frame(self.set_frame)
        self.set_entry_frame3.grid(column=1, row=0, padx=(10, 20), pady=0, sticky='nsew')

        self.arrow_label = ttk.Label(self.set_entry_frame3, text=" ", font=("Trebuchet MS", 12))
        self.arrow_label.grid(column=0, row=0, padx=2, pady=10, sticky='nsew')

        self.arrow_label = ttk.Label(self.set_entry_frame3, text="→", font=("Trebuchet MS", 25))
        self.arrow_label.grid(column=0, row=1, padx=2, pady=0, sticky='nsew')

        # Center Arrow ========================================================================================================/\ /\ /\

        # Set Entry 2 Frame ===================================================================================================\/ \/ \/
        self.set_entry_frame2 = ttk.Frame(self.set_frame)
        self.set_entry_frame2.grid(column=3, row=0, padx=(0, 20), pady=0, sticky='nsew')

        self.arrow_label2 = ttk.Label(self.set_entry_frame2, text="PC", font=("Trebuchet MS", 25, "bold"))
        self.arrow_label2.grid(column=0, row=0, padx=0, pady=(10, 0), sticky='nsew')

        # create trash button to reset string
        self.trash_button2 = ttk.Button(self.set_entry_frame2, text="🗑️", command=self.reset_button_name_var, style="Custom.TButton", width=3)
        self.trash_button2.grid(column=0, row=0, padx=0, pady=(0, 0), sticky='se')

        self.button_name_var2 = tk.StringVar()
        self.entry2 = ttk.Entry(self.set_entry_frame2, textvariable=self.button_name_var2, width=34, font=("Trebuchet MS", 13), style="Custom.TEntry", state='readonly', cursor='arrow')
        self.entry2.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')
        # Set Entry 2 Frame ===================================================================================================/\ /\ /\
        # Set Bind Frame ===============================================================================================================/\ /\ /\
        # Mid Row ================================================================================================================================/\ /\ /\
        # Main frame ======================================================================================================================================/\ /\ /\

        self.update_centering_pad()
        self.update_idletasks()  # Ensure the window is updated before getting the size # Call the update_centering_pad method
        self.bind('<Configure>', self.update_centering_pad)
        self.update_status()
        self.canvas.bind('<Button-1>', self.on_canvas_click)  # Bind the canvas click event

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
        image_frame_width = self.image_frame.winfo_width()
        binds_frame_width = self.binds_frame.winfo_width()
        set_frame_width = self.set_frame.winfo_width()

        difference = window_width - image_frame_width - binds_frame_width - 40
        if difference > 0:
          padx = difference // 4
          self.centering_pad.grid_configure(padx=padx)

        difference = window_width - set_frame_width + 33
        if difference > 3:
          padx = difference // 4
          self.centering_pad2.grid_configure(padx=padx)
            

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
                self.button_name_var.set(xbox_bind_string)  # Update the text in the first Entry widget


            
    def reset_button_name_var(self, event=None):
        self.button_name_var.set("")
        self.current_macro.xbox_binds = []

class Macro():
    def __init__(self):
        self.xbox_binds = []
        self.pc_binds = []
        self.sequence = False
    
    def add_bind(self, xbox_bind):
        self.xbox_binds.append(xbox_bind)

if __name__ == "__main__":
    app = App()
    app.mainloop()






      
        