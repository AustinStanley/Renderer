# Stanley, R. Austin
# 1000-855-734
# 2016-03-02
# Assignment_02

import numpy as np
import time

from tkinter import *
from math import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

class cl_widgets:
    def __init__(self,ob_root_window,ob_world=[]):
        self.ob_root_window=ob_root_window
        self.ob_world=ob_world
        #self.menu=cl_menu(self)
        self.toolbar=cl_toolbar(self)
        self.pannel_01 = cl_pannel_01(self)
        self.pannel_02 = cl_pannel_02(self)
        self.ob_canvas_frame=cl_canvas_frame(self)
        #self.status = cl_statusBar_frame(self)
        self.ob_world.add_canvas(self.ob_canvas_frame.canvas)
        self.verteces = []
        self.faces = []
        self.window = None
        self.viewport = None

class cl_canvas_frame:
    def __init__(self, master):
        self.master=master
        self.canvas = Canvas(master.ob_root_window,width=640, height=640, bg="white", highlightthickness=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        
        self.canvas.bind('<Configure>', self.canvas_resized_callback) 
        self.canvas.bind("<ButtonPress-1>", self.left_mouse_click_callback)
        #self.canvas.bind("<ButtonRelease-1>", self.left_mouse_release_callback)
        #self.canvas.bind("<B1-Motion>", self.left_mouse_down_motion_callback)
        #self.canvas.bind("<ButtonPress-3>", self.right_mouse_click_callback)
        #self.canvas.bind("<ButtonRelease-3>", self.right_mouse_release_callback)
        #self.canvas.bind("<B3-Motion>", self.right_mouse_down_motion_callback)
        #self.canvas.bind("<Key>", self.key_pressed_callback)    
        self.canvas.bind("<Up>", self.up_arrow_pressed_callback)
        self.canvas.bind("<Down>", self.down_arrow_pressed_callback)
        self.canvas.bind("<Right>", self.right_arrow_pressed_callback)
        self.canvas.bind("<Left>", self.left_arrow_pressed_callback)     
        self.canvas.bind("<Shift-Up>", self.shift_up_arrow_pressed_callback)
        self.canvas.bind("<Shift-Down>", self.shift_down_arrow_pressed_callback)
        self.canvas.bind("<Shift-Right>", self.shift_right_arrow_pressed_callback)
        self.canvas.bind("<Shift-Left>", self.shift_left_arrow_pressed_callback)   
        self.canvas.bind("f", self.f_key_pressed_callback)  
        self.canvas.bind("b", self.b_key_pressed_callback)  
    def key_pressed_callback(self,event):
        print ('key pressed')      
    def up_arrow_pressed_callback(self,event):
        print ('pressed up')
        
    def down_arrow_pressed_callback(self,event):
        print ('pressed down')     
    def right_arrow_pressed_callback(self,event):
        print ('pressed right')       
    def left_arrow_pressed_callback(self,event):
        print ('pressed left')       
    def shift_up_arrow_pressed_callback(self,event):
        self.canvas.world.translate(0,.1,0,1)
    def shift_down_arrow_pressed_callback(self,event):
        pass
    def shift_right_arrow_pressed_callback(self,event):
        pass
    def shift_left_arrow_pressed_callback(self,event):
        pass
    def f_key_pressed_callback(self,event):

        print ("f key was pressed")
    def b_key_pressed_callback(self,event):
        
        print ("b key was pressed")         
    def left_mouse_click_callback(self,event):
        print ('Left mouse button was clicked')
        print ('x=',event.x, '   y=',event.y)
        
        
        self.x = event.x
        self.y = event.y  
        self.canvas.focus_set()
    def left_mouse_release_callback(self,event):
        print ('Left mouse button was released')
        print ('x=',event.x, '   y=',event.y)
        print ('canvas width', self.canvas.cget("width"))
        self.x = None
        self.y = None
        
    def left_mouse_down_motion_callback(self,event):
        print ('Left mouse down motion')
        print ('x=',event.x, '   y=',event.y)
        self.x = event.x
        self.y = event.y 
        
    def right_mouse_click_callback(self,event):
        
        self.x = event.x
        self.y = event.y   
    def right_mouse_release_callback(self,event):
        
        self.x = None
        self.y = None        
    def right_mouse_down_motion_callback(self,event):
        pass
    def canvas_resized_callback(self,event):
        self.canvas.config(width=event.width,height=event.height)
        #self.canvas.config(width=event.width-4,height=event.height-4)
        #print 'canvas width height', self.canvas.cget("width"), self.canvas.cget("height")
        #print 'event width height',event.width, event.height
        
        self.canvas.pack()
        print ('canvas width', self.canvas.cget("width"))
        print ('canvas height', self.canvas.cget("height"))
        self.master.ob_world.redisplay(self.master.ob_canvas_frame.canvas,event)
        
class cl_toolbar:
    def __init__(self, master):
        
        self.master=master
        frame = Frame(master.ob_root_window)
        frame.pack()
        
        self.var_filename = StringVar()
        self.var_filename.set('')
        
        # define GUI elements
        self.label_fname = Label(frame, text='Filename: ')        
        self.entry = Entry(frame, width=50, textvariable=self.var_filename)        
        self.btn_browse = Button(frame, text='Browse', command=self.browse_file)
        self.btn_load = Button(frame, text='Load', command=self.load)
        
        # pack GUI elements
        self.label_fname.pack(side=LEFT)
        self.entry.pack(side=LEFT)
        self.btn_browse.pack(side=LEFT)
        self.btn_load.pack(side=LEFT)
        
    def browse_file(self):
        self.var_filename.set(filedialog.askopenfilename(filetypes=[("allfiles","*"),("pythonfiles","*.txt")]))
    
    def load(self):
        filename = self.var_filename.get()
        
        if not filename:
            messagebox.showwarning('Error', 'No file specified')
            return
        
        with open(filename, 'r') as f:
            data = [l for l in f.read().splitlines() if l]
            
        del self.master.verteces[:]
        del self.master.faces[:]
        
        for l in data:
            points = l.split()[1:]
            if l[0] == 'v':
                self.master.verteces.append(np.array(points).astype(float))
            elif l[0] == 'f':
                self.master.faces.append([int(x) for x in points])
            elif l[0] == 'w':
                self.master.window = tuple(float(x) for x in points)
            elif l[0] == 's':
                self.master.viewport = tuple(float(x) for x in points)
            else:
                messagebox.showerror('Error', 'Invalid file format')
                return
                
        self.master.ob_world.draw(self.master.ob_canvas_frame.canvas, 
                                  self.master.verteces, 
                                  self.master.faces, 
                                  self.master.window, 
                                  self.master.viewport)
        
class cl_pannel_01:

    def __init__(self, master):

        self.master=master
        frame = Frame(master.ob_root_window)
        frame.pack()
        
        self.var_axis = StringVar()
        self.var_axis.set('')
        
        # define GUI elements
        self.label_rotaxis = Label(frame, text='Rotation Axis: ')
        self.label_degree = Label(frame, text='Degrees: ')
        self.label_steps = Label(frame, text='Steps: ')
        self.rdo_x = Radiobutton(frame, text='X', variable=self.var_axis, value='x')
        self.rdo_y = Radiobutton(frame, text='Y', variable=self.var_axis, value='y')
        self.rdo_z = Radiobutton(frame, text='Z', variable=self.var_axis, value='z')
        #self.rdo_ab = Radiobutton(frame, text='Line AB', variable=self.var_axis, value='ab')
        self.spnbox_degree = Spinbox(frame, from_=0, to=360, width=3)
        self.spnbox_steps = Spinbox(frame, from_=1, to=10, width=2)
        self.btn_rotate = Button(frame, text='Rotate', command=self.btn_rotate_callback)
        
        # pack GUI elements
        self.label_rotaxis.pack(side=LEFT)
        self.rdo_x.pack(side=LEFT)
        self.rdo_y.pack(side=LEFT)
        self.rdo_z.pack(side=LEFT)
        #self.rdo_ab.pack(side=LEFT)
        self.label_degree.pack(side=LEFT)
        self.spnbox_degree.pack(side=LEFT)
        self.label_steps.pack(side=LEFT)
        self.spnbox_steps.pack(side=LEFT)
        self.btn_rotate.pack(side=LEFT)
        
        self.rdo_z.select()
        
    def btn_rotate_callback(self):
        axis = self.var_axis.get()
        steps = int(self.spnbox_steps.get())
        theta = np.deg2rad(int(self.spnbox_degree.get())) / steps
        
        for n in range(steps):
            self.master.verteces = self.master.ob_world.rotate(axis, theta, self.master.verteces)
            self.master.ob_world.draw(self.master.ob_canvas_frame.canvas, 
                                      self.master.verteces, 
                                      self.master.faces, 
                                      self.master.window, 
                                      self.master.viewport)
            time.sleep(1/60)
    
class cl_pannel_02:

    def __init__(self, master):

        self.master=master
        frame = Frame(master.ob_root_window)
        frame.pack()
        
        self.var_radiosel = StringVar(value='')
        self.var_sx = StringVar(value='1.0')
        self.var_sy = StringVar(value='1.0')
        self.var_sz = StringVar(value='1.0')
        self.var_a1 = StringVar(value='0.0')
        self.var_a2 = StringVar(value='0.0')
        self.var_a3 = StringVar(value='0.0')
        
        #define GUI elements
        self.label_ratio = Label(frame, text='Scale Ratio: ')
        self.label_about = Label(frame, text='A: ')
        self.label_steps = Label(frame, text='Steps')
        self.rdo_all = Radiobutton(frame, text='All', variable=self.var_radiosel, value='a')
        self.rdo_vector = Radiobutton(frame, text='[Sx, Sy, Sz]: ', variable=self.var_radiosel, value='v')
        self.spnbox_ratio = Spinbox(frame, from_=0.0, to=4.0, width=4, increment=0.25, format='%1.2f')
        self.spnbox_steps = Spinbox(frame, from_=0, to=10, width=2)
        self.entry_sx = Entry(frame, width=3, textvariable=self.var_sx)
        self.entry_sy = Entry(frame, width=3, textvariable=self.var_sy)
        self.entry_sz = Entry(frame, width=3, textvariable=self.var_sz)
        self.entry_a1 = Entry(frame, width=3, textvariable=self.var_a1)
        self.entry_a2 = Entry(frame, width=3, textvariable=self.var_a2)
        self.entry_a3 = Entry(frame, width=3, textvariable=self.var_a3)
        self.btn_scale = Button(frame, text='Scale', command=self.btn_scale_callback)
        
        # pack GUI elements
        self.label_ratio.pack(side=LEFT)
        self.rdo_all.pack(side=LEFT)
        self.spnbox_ratio.pack(side=LEFT)
        self.rdo_vector.pack(side=LEFT)
        self.entry_sx.pack(side=LEFT)
        self.entry_sy.pack(side=LEFT)
        self.entry_sz.pack(side=LEFT)
        self.label_about.pack(side=LEFT)
        self.entry_a1.pack(side=LEFT)
        self.entry_a2.pack(side=LEFT)
        self.entry_a3.pack(side=LEFT)
        self.label_steps.pack(side=LEFT)
        self.spnbox_steps.pack(side=LEFT)
        self.btn_scale.pack(side=LEFT)
        
        self.rdo_all.select()
        
    def btn_scale_callback(self):
        if self.var_radiosel.get() == 'a':
            scale = float(self.spnbox_ratio.get())
            scale_vector = np.array((scale, scale, scale))
        elif self.var_radiosel.get() == 'v':
            scale_vector = np.array((float(self.entry_sx.get()), float(self.entry_sy.get()), float(self.entry_sz.get())))
        
        point = (float(self.entry_a1.get()), float(self.entry_a2.get()), float(self.entry_a3.get()))
        steps = int(self.spnbox_steps.get())
        
        scale_factor = (scale_vector - 1) / steps
        
        for n in range(steps):
            scaled_verts = self.master.ob_world.scale(point, np.array([1, 1, 1]) + scale_factor * n, self.master.verteces)
            self.master.ob_world.draw(self.master.ob_canvas_frame.canvas, 
                                          scaled_verts, 
                                          self.master.faces, 
                                          self.master.window, 
                                          self.master.viewport)
            time.sleep(1/60)
            
        self.master.verteces = scaled_verts
        
class MyDialog(simpledialog.Dialog):
    def body(self, master):

        Label(master, text="Integer:").grid(row=0, sticky=W)
        Label(master, text="Float:").grid(row=1, column=0 ,sticky=W)
        Label(master, text="String:").grid(row=1, column=2 , sticky=W)
        self.e1 = Entry(master)
        self.e1.insert(0, 0)
        self.e2 = Entry(master)
        self.e2.insert(0, 4.2)
        self.e3 = Entry(master)
        self.e3.insert(0, 'Default text')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=1, column=3)
        
        
        self.cb = Checkbutton(master, text="Hardcopy")
        self.cb.grid(row=3, columnspan=2, sticky=W)


    def apply(self):
        try:
            first = int(self.e1.get())
            second = float(self.e2.get())
            third=self.e3.get()
            self.result = first, second, third
        except ValueError:
            messagebox.showwarning(
                "Bad input",
                "Illegal values, please try again"
            )


#class StatusBar:

    #def __init__(self, master):
        #self.master=master
        #self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        #self.label.pack(fill=X)

    #def set(self, format, *args):
        #self.label.config(text=format % args)
        #self.label.update_idletasks()

    #def clear(self):
        #self.label.config(text="")
        #self.label.update_idletasks()       

class cl_statusBar_frame:

    def __init__(self, master):
        self.master=master
        status = StatusBar(master.ob_root_window)
        status.pack(side=BOTTOM, fill=X)
        status.set('%s','This is the status bar')


    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
class cl_menu:
    def __init__(self, master):
        
        self.master=master
        self.menu = Menu(master.ob_root_window)
        master.ob_root_window.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.menu_callback)
        self.filemenu.add_command(label="Open...", command=self.menu_callback)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.menu_callback)
        self.dummymenu = Menu(self.menu)
        self.menu.add_cascade(label="Dummy", menu=self.dummymenu)
        self.dummymenu.add_command(label="Item1", command=self.menu_item1_callback)
        self.dummymenu.add_command(label="Item2", command=self.menu_item2_callback)
        
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About...", command=self.menu_help_callback)        

    def menu_callback(self):
        print ("called the menu callback!")
                        
    def menu_help_callback(self):
        print ("called the help menu callback!") 
    def menu_item1_callback(self):
        print ("called item1 callback!")    

    def menu_item2_callback(self):
        print ("called item2 callback!")    


