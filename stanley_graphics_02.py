# Stanley, R. Austin
# 1000-855-734
# 2016-03-02
# Assignment_02

import numpy as np
from numpy  import *
from math import *
from tkinter import *

def window_to_viewport(point, window, viewport, canvas):
    wxmin, wymin, wxmax, wymax = window
    vxmin, vymin, vxmax, vymax = viewport
    xres = float(canvas.cget('width'))
    yres = float(canvas.cget('height'))
    
    vxmin *= xres
    vxmax *= xres
    vymin *= yres
    vymax *= yres
    
    xratio = (vxmax - vxmin) / (wxmax - wxmin)
    yratio = (vymax - vymin) / (wymax - wymin)
    
    # homogeneous coords
    point = np.append(point, 1)
    
    M_wv = np.matrix([[xratio, 0, -wxmin * xratio + vxmin],
                      [0, yratio, -wymin * yratio + vymin],
                      [0, 0, 1]])
                      
    res = M_wv.dot(point).getA()[0][:-1]
    res[1] = yres - res[1]
    return tuple(res)
    
def window_to_viewport2(points, window, viewport, canvas):
    wxmin, wymin, wxmax, wymax = window
    vxmin, vymin, vxmax, vymax = viewport
    xres = float(canvas.cget('width'))
    yres = float(canvas.cget('height'))
    
    t1 = np.matrix([[1, 0, -wxmin], [0, 1, -wymin], [0, 0, 1]])
    t2 = np.matrix([[1, 0, vxmin], [0, 1, vymin], [0, 0, 1]])
    s1 = np.matrix([[(vxmax - vxmin) / (wxmax - wxmin), 0, 0], [0, (vymax - vymin) / (wymax - wymin), 0], [0, 0, 1]])
    s2 = np.matrix([[xres, 0, 0], [0, yres, 0], [0, 0, 1]])
    
    res = []
    for p in points:
        #p = np.append(p, 1) # homogeneous coords
        p[2] = 1
    
        mapped_point = t1.dot(p).dot(s1).dot(t2).dot(s2).getA()[0]
        mapped_point[1] = (vymax * yres) - mapped_point[1]
    
        res.append(tuple(mapped_point[:-1]))
    
    return res
    


class cl_world:
    def __init__(self, objects=[],canvases=[]):
        self.objects=objects
        self.canvases=canvases
        #self.display
        
 
    def add_canvas(self,canvas):
        self.canvases.append(canvas)
        canvas.world=self
    
    def create_graphic_objects(self,canvas):
        self.objects.append(canvas.create_line(0,0,canvas.cget("width"),canvas.cget("height")))
        self.objects.append(canvas.create_line(canvas.cget("width"),0,0,canvas.cget("height")))
        self.objects.append(canvas.create_oval(int(0.25*int(canvas.cget("width"))),
            int(0.25*int(canvas.cget("height"))),
            int(0.75*int(canvas.cget("width"))),
            int(0.75*int(canvas.cget("height")))))
            
    def draw(self, canvas, verteces, faces, window, viewport):
        canvas.delete(ALL)            
        del self.objects[:]
        
        # draw viewport
        self.objects.append(canvas.create_rectangle(round(float(canvas.cget('width')) * viewport[0]),
                                                    round(float(canvas.cget('height')) * viewport[1]),
                                                    round(float(canvas.cget('width')) * viewport[2]),
                                                    round(float(canvas.cget('height')) * viewport[3])))
        
        # map verteces to the viewport, then draw
        for f in faces:
            current_verts = [verteces[i - 1][:-1] for i in f]
            mapped_verts = []
            
            for v in current_verts:
                mapped_verts.append(window_to_viewport(v, window, viewport, canvas))
                
            self.objects.append(canvas.create_polygon(mapped_verts, fill="red", outline="black"))
            
        # save data for redisplay
        self.verteces = verteces
        self.faces = faces
        self.window = window
        self.viewport = viewport
        
        canvas.update_idletasks()
        
    def draw2(self, canvas, verteces, faces, window, viewport):
        for o in self.objects:
            canvas.delete(o)
            
        del self.objects[:]
        
        # draw viewport
        self.objects.append(canvas.create_rectangle(round(float(canvas.cget('width')) * viewport[0]),
                                                    round(float(canvas.cget('height')) * viewport[1]),
                                                    round(float(canvas.cget('width')) * viewport[2]),
                                                    round(float(canvas.cget('height')) * viewport[3])))
                                                    
        mapped_verts = window_to_viewport2(verteces, window, viewport, canvas)
        
        for f in faces:
            current_verts = [mapped_verts[i - 1] for i in f]                
            self.objects.append(canvas.create_polygon(current_verts, fill="red", outline="black"))
            
        # save data for redisplay
        self.verteces = verteces
        self.faces = faces
        self.window = window
        self.viewport = viewport
        
    def rotate(self, axis, theta, verteces):
        if axis == 'x':
            r = np.matrix([[1, 0, 0],
                           [0, np.cos(theta), -np.sin(theta)],
                           [0, np.sin(theta), np.cos(theta)]])
        elif axis == 'y':
            r = np.matrix([[np.cos(theta), 0, np.sin(theta)],
                           [0, 1, 0],
                           [-np.sin(theta), 0, np.cos(theta)]])
        elif axis == 'z':
            r = np.matrix([[np.cos(theta), -np.sin(theta), 0],
                           [np.sin(theta), np.cos(theta), 0],
                           [0, 0, 1]])
                           
        new_verts = []
        for v in verteces:
            new_verts.append(r.dot(v).getA()[0])
            
        return new_verts
        
    def scale(self, point, scale_vector, verteces):
        t1 = np.matrix([[1, 0, 0, -point[0]], 
                        [0, 1, 0, -point[1]], 
                        [0, 0, 1, -point[2]], 
                        [0, 0, 0, 1]])
                        
        t2 = np.matrix([[1, 0, 0, point[0]], 
                        [0, 1, 0, point[1]], 
                        [0, 0, 1, point[2]], 
                        [0, 0, 0, 1]])
                        
        s = np.matrix([[scale_vector[0], 0, 0, 0], 
                       [0, scale_vector[1], 0, 0], 
                       [0, 0, scale_vector[2], 0], 
                       [0, 0, 0, 1]])
                       
        new_verts = []
        for v in verteces:
            homogeneous_v = np.append(v, 1)
            new_verts.append(t2.dot(s.dot(t1.dot(homogeneous_v).getA()[0]).getA()[0]).getA()[0][:-1])
            
        return new_verts
                           
        
    def redisplay(self,canvas,event):
        if self.objects:
            self.draw(canvas, self.verteces, self.faces, self.window, self.viewport)