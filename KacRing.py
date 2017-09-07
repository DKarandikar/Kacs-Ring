##Kac Ring Model

import random
import math
import time

import tkinter as tk
from tkinter import ttk

# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(tk.Canvas):
    def __init__(self,parent,**kwargs):
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        #self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        #self.scale("all",0,0,wscale,hscale)
    
    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r,tags="circle", **kwargs)
        
        
class col_circle():
    '''This is a circle that travels round the ring'''
    def __init__(self,location,x,y,r,N):
        self.x = x
        self.y = y
        self.N = N
        self.theta = (location/self.N)*math.pi*2
        self.location = location
        self.r = r
        
        self.radius = 10
        self.fill = "white"
    
    def draw(self,canvas,t):
        canvas.create_circle(self.x + int(self.r * math.cos(((self.location+t/10)/self.N)*math.pi*2)),
                             self.y + int(self.r * math.sin(((self.location+t/10)/self.N)*math.pi*2)),
                              self.radius,fill = self.fill)

    def change(self):
        if self.fill == "white":
            self.fill = "black"
        else:
            self.fill = "white"
            
    def move(self):
        self.location = (self.location + 1)%self.N

class marker():
    '''This is a static marker'''
    def __init__(self,x,y,location,r,N):
        self.x = x
        self.y = y
        self.N = N
        self.theta = ((location)/self.N)*math.pi*2
        self.location = location
        self.r = r
        
    def draw(self,canvas):
        points = [self.x + int(self.r * math.cos((self.theta))),self.y + int(self.r * math.sin((self.theta))),
                  self.x + int((self.r+30) * math.cos((self.theta+0.1))),self.y + int((self.r+30) * math.sin((self.theta+0.1))),
                  self.x + int((self.r+30) * math.cos((self.theta-0.1))), self.y + int((self.r+30) * math.sin((self.theta-0.1)))]
        canvas.create_polygon(points,width=1,fill="white",outline="black")
    
class App(tk.Tk): 
    '''The main Kac Ring App'''    
    def __init__(self):
        tk.Tk.__init__(self)

        # setup all the indep. variables         
        self.N = 25
        self.n = 10
        self.x = 300
        self.y = 300
        self.r = 200
        
        # setup the dep. and operational variables
        
        self.W = self.N
        self.B = 0
        self.w = self.n
        self.b = 0
        
        self.circles = []
        self.markers = []
        self.marker_locations = []
        while len(self.marker_locations) < self.n:
            self.marker_locations.append(random.randint(0,self.N-1)+0.5)
        
        
        self.autoOn = False
        self.transition = 0
        
        # start building visual elements
        
        self.myframe = tk.Frame(self)
        self.myframe.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.myframe.rowconfigure(0,weight=1)
        self.myframe.columnconfigure(0,weight=1)
        
        self.mybutton = tk.Button(self.myframe,text="Reset",command = self.reset)
        self.mybutton.grid(row=0,column=0)
        
        self.button1 = ttk.Button(self.myframe, text="Auto: Off",command=lambda: self.auto(True))
        self.button1.grid(row=2,column=0)
        
        self.mycanvas = ResizingCanvas(self.myframe,width=2*self.x, height=2*self.y, bg="white", highlightthickness=0)
        self.mycanvas.grid(row=1,column=0)
        
        # add the widgets
        for x in range(self.N):
            self.circles.append(col_circle(x,self.x,self.y,self.r,self.N))
            
        for circle in self.circles:
            circle.draw(self.mycanvas,0)
            
        for location in self.marker_locations:    
            self.markers.append(marker(self.x,self.y,location,self.r,self.N))
            
        for k in self.markers:
            k.draw(self.mycanvas)
            
        # tag all of the drawn widgets
        self.mycanvas.addtag_all("all")
        
    def reset(self):
        self.circles = []
        self.markers = []
        self.marker_locations = set()
        while len(self.marker_locations) < self.n:
            self.marker_locations |= {(random.randint(0,self.N-1)+0.5)}
        self.marker_locations = list(self.marker_locations)
        
        
        self.autoOn = False
        self.transition = 0
        
        self.mycanvas.delete("all")
        
        for x in range(self.N):
            self.circles.append(col_circle(x,self.x,self.y,self.r,self.N))
            
        for circle in self.circles:
            circle.draw(self.mycanvas,0)
            
        for location in self.marker_locations:    
            self.markers.append(marker(self.x,self.y,location,self.r,self.N))
            
        for k in self.markers:
            k.draw(self.mycanvas)
            
        # tag all of the drawn widgets
        self.mycanvas.addtag_all("all")
        
        
    def auto(self,click):
        '''Controls the automatic function, click tells us whether the call was from the button or from the .after method'''
        
        if click: #Turns it on/off if the button was pressed, otherwise just keeps ticking along
            self.autoOn = not self.autoOn  
        if self.autoOn:
            self.button1.config(text="Auto: On")
            self.tick()
            self.after(50,lambda: self.auto(False))
            
        else:
            self.button1.config(text="Auto: Off")
            
    def tick(self):
        '''Occurs every 50ms when the auto is running, moves the circles and colours them'''
        self.mycanvas.grid_forget()
        self.transition +=1
        self.mycanvas.delete("circle")
        
        if self.transition == 10:
            self.transition = 0 
            for circle in self.circles:
                circle.move()
                
        elif self.transition == 5:
            for circle in self.circles:
                if any(circle.location == int((marker.location - 0.5)) for marker in self.markers):
                    circle.change()
                    
        for circle in self.circles:
            circle.draw(self.mycanvas,self.transition)
        self.mycanvas.grid(row=1,column=0)
            
        
myApp = App()
myApp.mainloop()