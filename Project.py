import tkinter as tk
from tkinter import *
from anytree import Node
import random
import signal
#********************************************************************************************************************

class GameBoard(tk.Frame):
    def __init__(self, parent, player, rows=10, columns=10, size=60, color1="white", color2="blue"):
        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.places = {}
        self.player = player
        self.playercoords = (10 ,10)
        canvas_width = columns * size
        canvas_height = rows * size
        tk.Frame.__init__(self, parent)
        self.startbutton = tk.Button(self , text = 'start' , command = self.move)
        self.startbutton.pack()
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
            width=canvas_width, height=canvas_height, background="black")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = (y1 + self.size)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color  , tags =str((row*10+col)+1))
                self.places[row*10+col+1] = [row , col]
                color = self.color1 if color == self.color2 else self.color2
        self.canvas.bind("<Button-1>",self.set_source)
        if player == 'Pawn':
            self.image = 'Pawn.png'
            self.imagedata = tk.PhotoImage(file = self.image)
        elif player == 'Knight':
            self.image = 'Knight.png'
            self.imagedata = tk.PhotoImage(file = self.image)
            
        
            
                
    def addpiece(self, name, image, row=0, column=0):
        self.canvas.create_image(0,0, image=image, tags=('player'), anchor="c")
        self.player = name
        self.placepiece(row, column)
        
    def placepiece(self, row, column):
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords('player', x0, y0)
        self.playercoords = (x0 , y0)

    def set_source(self , event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.source = self.places[self.canvas.find_closest(x, y)[0]]
        self.addpiece(self.player , self.imagedata , row =self.places[self.canvas.find_closest(x, y)[0]][0] , column =self.places[self.canvas.find_closest(x, y)[0]][1])
        self.canvas.bind("<Button-1>",self.set_destination)
        self.source = tuple(self.source)
        
        
        
    def set_destination(self , event):
        self.canvas.find_all()
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.destination = self.places[self.canvas.find_closest(x, y)[0]]
        self.destination = tuple(self.destination)
        if (self.canvas.find_withtag(CURRENT)):
            self.canvas.itemconfig(CURRENT , fill = 'red')
            self.canvas.bind("<Button-1>",self.disable)
        
    def disable(self , event):
        self.canvas.find_all()
        if (self.canvas.find_withtag(CURRENT)):
            self.canvas.itemconfig(CURRENT , fill = 'gray')
            self.places[int(self.canvas.gettags(CURRENT)[0])].append("block")

            
            

    def get_knight_moves(self,x,ps):
        l = []
        if [x[0]+1,x[1]+2] in ps:
            l.append((x[0]+1,x[1]+2))
        if [x[0]-1,x[1]+2] in ps:
            l.append((x[0]-1,x[1]+2))
        if [x[0]+2,x[1]+1] in ps:
            l.append((x[0]+2,x[1]+1))
        if [x[0]+2,x[1]-1] in ps:        
            l.append((x[0]+2,x[1]-1))
        if [x[0]+1,x[1]-2] in ps:
            l.append((x[0]+1,x[1]-2))
        if [x[0]-1,x[1]-2] in ps:    
            l.append((x[0]-1,x[1]-2))
        if [x[0]-2,x[1]-1] in ps:
            l.append((x[0]-2,x[1]-1))
        if [x[0]-2,x[1]+1] in ps:        
            l.append((x[0]-2,x[1]+1))
        return l

    def get_pawn_moves(self,x,ps):
        l = []
        if(([x[0]-1,x[1]] in ps)):
            l.append((x[0]-1,x[1]))
        if([x[0]-1,x[1]+1,'block'] in ps):
            l.append((x[0]-1,x[1]+1))
        if([x[0]+1,x[1]+1,'block'] in ps):
            l.append((x[0]+1,x[1]+1))
        if([x[0]+1,x[1]-1,'block'] in ps):
            l.append((x[0]+1,x[1]-1))
        if([x[0]-1,x[1]-1,'block'] in ps):
            l.append((x[0]-1,x[1]-1))
        return l



    def search(self):
        if self.player == 'Knight':
            get_moves = self.get_knight_moves
        else :
            get_moves = self.get_pawn_moves
        def h(x):
            return  abs(x[0] - self.destination[0]) + abs(x[1] - self.destination[1])
        def sort(l):
            return sorted(l,key = lambda x : x.data)
        root = Node(name = str(tuple(self.source)),data = h(self.source),pos = self.source)
        fring = []
        fring.append(root)
        flag = True
        while( flag):
            node = fring.pop(0)
            if node.pos == self.destination:
                flag = False
                l = []
                for i in node.ancestors:
                    l.append(i.pos)
                l.append(node.pos)
                return l
            else:
                for child in get_moves(node.pos,self.places.values()):
                    fring.append(Node(name = str(tuple(child)),pos = child,data = h(child)+((node.depth+1)*3),parent = node ))
                    
                    
                fring = sort(fring)

            
    def move(self):
        def signal_handler(signum, frame):
            raise Exception("Timed out!")
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(60)
        
        d = []
        for i in self.places:
            if len(self.places[i]) != 3 :
                d.append(i)
        k = 100 - len(d)
        if k < 20:
            while(k<21):
                k +=1
                t = random.choice(d)
                self.places[t].append('block')
                self.canvas.itemconfig(t , fill = 'gray')
        try :
            l = self.search()
        except Exception:
            l = []
        if (l):
            for i in l:
                self.after(1000)
                self.placepiece(i[0] , i[1])
                self.canvas.itemconfig(i[0]*10+i[1]+1 , fill = 'green')
                self.update()
#********************************************************************************************************************

def select():
    if v.get() == 3:
        name = 'Pawn'
    elif v.get() == 2:
        name = 'Knight'
    first.destroy()
        
    main = tk.Tk()
    main.title(name)
    board = GameBoard(main,name)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    main.mainloop()
    
        
first = tk.Tk()
sign_image = tk.PhotoImage(file = 'sign1.png')
sign = tk.Label(first,image = sign_image)
sign.pack()
v = tk.IntVar()       
r2 = tk.Radiobutton(first , text = 'knight', variable = v , value = 2, command = select).pack()
r3 = tk.Radiobutton(first , text = 'pawn', variable = v , value = 3, command = select).pack()
    
