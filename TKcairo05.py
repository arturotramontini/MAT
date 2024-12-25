# region IMPORTS
import dati
import test4
import colorsys
import math
import numpy as np
import cairo
from numba import njit
from numba import jit, prange
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter, ImageDraw
from PIL import ImageDraw, ImageFont

import Mandel

import time

import threading

import os
os.system('clear')


# endregion


# art of code, smooth iteration minute 20:00 ~
# https://www.youtube.com/watch?v=zmWkhlocBRY&t=6s


# region class App1 ----------------------------------------------------------------------------
# Funzione di callback

class CL_App1():

    jjj = "ioa"

    def __init__(self, root):

        # dati.CLdati.var2[0] = 0
        # progress = dati.CLdati.var2
        # self.monitor_thread = threading.Thread(target=dati.monitor_progress, args=(progress,))
        # self.monitor_thread.start()

        # Creazione dell'array al di fuori della funzione
        self.array8 = np.zeros(64, dtype=np.complex128)
        self.array8Cnt = 0

        self.xyz = "cippolo"
        self.counter2 = 2000

        self.distRadius = 30

        self.root = root

        # Definizione della larghezza e altezza del mandelbrot image
        # self.widthImg, self.heightImg = 12000 , 12000 # 3840,2160        
        self.widthImg, self.heightImg = 12000 , 12000 # 3840,2160        
        self.width, self.height = 1000, 1000
        # Imposta dimensioni e posizione della finestra (larghezza x altezza + x + y)
        self.root.geometry("1300x1600+0+0")

        self.root.title("Esempio di Canvas con widget in una classe")
        self.root.title("Esempio Cairo con Tk")
        root.configure(bg="#404040")  # Colore di sfondo

        # Funzione che aggiorna le coordinate del mouse nel campo di testo
        self.mouseX = int(self.width / 2)
        self.mouseY = int(self.height / 2)

        self.MandelRadius = 1.3
        self.MandelCx = 0
        self.MandelCy = 0
        self.MandelCxP = -0.75
        self.MandelCyP = 0

        self.RADICE = 1000

        cairoW, cairoH = 600, 500
        # Creazione di una superficie Cairo in memoria
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, cairoW, cairoH)  # self.width, self.height)

        self.context = cairo.Context(self.surface)

        self.draw()

        # Conversione della superficie Cairo in un'immagine PIL (?Tk)
        self.image = Image.frombuffer(
            "RGBA",
            (cairoW, cairoH),
            self.surface.get_data(),
            "raw",
            "BGRA", 0, 1
        )
        resized_img = self.image.resize((self.width, self.height))
        # resized_img = self.image.resize((100, 300))

        # Creazione di una Label per l'immagine di sfondo
        self.tk_image = ImageTk.PhotoImage(resized_img)
        # self.tk_image = ImageTk.PhotoImage(self.image)

        self.tk_image_5 = self.tk_image

        self.background_label = tk.Label(
            self.root, image=self.tk_image,  anchor="w")

        self.background_label = tk.Label(self.root,   anchor="w")
        # self.background_label.place(x=0, y=300, relwidth=.5, relheight=.5)  # Posiziona l'immagine come sfondo
        # Posiziona l'immagine come sfondo

        # self.background_label.place(x=100, y=1350)
        # # self.background_label.pack()  # Posiziona l'immagine come sfondo

        self.background_label.config(
            compound='center',

            text=f"label back: {
                12345.67}", font=("Courier", 34),
            image=self.tk_image,
        )

        # self.background_label.config(
        #     # compound='center',

        #     text=f"label back: {
        #         "ciccio"}", font=("Courier", 34),
        #     image=self.tk_image,
        # )

        self.imageSaved = self.image

        self.a = CL_mandelbrot(self)

        self.image = self.a.Mandelbrot(
            self.width, self.height, self.mouseX, self.mouseY)
        # self.image = np.zeros((self.height, self.width), dtype=np.uint32)
        # # Da immagine PIL a immagine Tk

        self.tk_image = ImageTk.PhotoImage(self.image)

        resized_img2 = self.image.resize((self.width, self.height))
        blend_image_5 = Image.blend(resized_img2, resized_img, alpha=0.5)

        # Mostra o salva il risultato
        # blend_image_5.show()

        resized_img3 = blend_image_5.resize((200, 200))

        # self.tk_image_6 = ImageTk.PhotoImage(blend_image_5)
        self.tk_image_6 = ImageTk.PhotoImage(resized_img3)

        self.tk_image_5 = self.tk_image_6
        self.background_label.config(
            image=self.tk_image_6,
        )
        dati.Tooltip(self.background_label, "background_label")

        # Visualizzazione dell'immagine in un'etichetta Tk
        self.label = tk.Label(
            self.root, image=self.tk_image, pady=0, bg="cyan")
        self.label.pack(pady=2, padx=2, side="top")
        dati.Tooltip(self.label, "label")

        self.fr0 = tk.Frame(self.root,bg='cyan')
        self.fr0.pack(padx=5, pady=5)


        # self.labelframe = tk.LabelFrame(self.root, text="rd cx cy", padx=10, pady=10,bg="red")
        self.labelframe = tk.LabelFrame(
            self.fr0, text="rd cx cy", padx=10, pady=10, bg="#800000")
        # anchor="w",fill="none")#side="top")
        self.labelframe.pack(padx=5, pady=5, anchor='ne')#side="right")



        self.oFrame1 = dati.CLframe1(self, self.root)
        self.oFrame2 = dati.CLframe2(self, self.root)

        # tk.Label(self.labelframe, text="RD").pack(side="top")
        # dati.Tooltip(self.labelframe, "labelframe")

        # Visualizzazione dell'immagine in un'etichetta Tk
        self.label4 = tk.Label(self.labelframe, text="label4",
                               bg="yellow")  # width=120,
        self.label4.pack(padx=0, pady=0, side="top")
        dati.Tooltip(self.label4, "label4")

        self.entry = tk.Entry(self.labelframe, font=(
            "Unifont", 12), width=20)  # 100)
        self.entry.pack(padx=0, pady=0, side="right")
        dati.Tooltip(self.entry, "entry")

        self.entry1 = tk.Entry(self.labelframe, text="1234")
        self.entry1.pack(padx=0, pady=0, side="left")
        self.entry1.bind('<KP_Enter>', self.e1cmd)
        self.entry1.bind('<Return>', self.e1cmd)
        dati.Tooltip(self.entry1, "widget: entry1")

    #     # Crea il Canvas e lo aggiunge alla finestra principale
    #     self.canvas = tk.Canvas(self.root, width=600, height=600, bg=None) # "#9f9f9f")
    #     self.canvas.place(x=5, y=150, width=500, height=300, bg=None)

    #     # Disegna un rettangolo
    #     self.canvas.create_rectangle(50, 50, 150, 150, fill="blue")
    #     # Disegna un cerchio (oval)
    #     self.canvas.create_oval(200, 50, 300, 150, fill="red")
    #     # Disegna una linea
    #     self.canvas.create_line(40, 40, 280, 230, fill="green", width=2)
    #     self.canvas.create_line(20, 20, 21, 21, fill="white", width=2)
    #    # Usa create_image per visualizzare l'immagine sul Canvas
    #     # Posiziona l'immagine al centro del Canvas
    #     # self.image_id = self.canvas.create_image(300, 300, image=self.tk_image)

    #     # Scrittura di testo nel Canvas
    #     self.canvas.create_text(0, 0, text="Testo sul Canvas", font=("Arial", 20), \
    #                             anchor="nw", fill="red")

        # self.counter = 10000

        # # Crea una label per mostrare il valore
        # self.label2 = tk.Label(self.root,bg=None, text=f"Valore: {
        #                        self.counter}", font=("Helvetica", 16))
        # # self.label2.pack(pady=2)
        # self.label2.place(x=0,y=0)

        # Creazione del pulsante
        self.button = tk.Button(self.labelframe, text="Premi me!",
                                command=self.on_button_click, font=("Arial", 14))
        self.button.pack(padx=5, pady=5,  side="left")
        dati.Tooltip(self.button, "button")

        self.var1 = tk.IntVar(value=0)
        self.checkbox_selection()
        self.c1 = tk.Checkbutton(self.labelframe, text='Python', variable=self.var1,
                                 onvalue=1, offvalue=0, command=self.checkbox_selection)
        self.c1.pack(padx=5, pady=5, side="bottom")
        
        dati.Tooltip(self.c1, "checkbox: c1")

        # Crea una label per mostrare il valore
        self.label3 = tk.Label(self.labelframe, text=f"label3: {
                               12345.67}", font=("Courier", 12))
        self.label3.pack(pady=2, side="right")
        # self.label3.place(x=0,y=100)
        dati.Tooltip(self.label3, "label3")

        # # Visualizzazione dell'immagine in un'etichetta Tk
        # self.label5 = tk.Label(self.root,  image=self.tk_image_5)
        # self.label5.pack()
        # dati.Tooltip(self.label5, "label5")

        # ---------- BINDING ----------

        # Associa ESC per uscire e A per ridisegnare
        self.root.bind("<Escape>", self.quit)
        self.root.bind("<a>", self.keyA)  # self.testOut)
        self.root.bind("<m>", self.keyM)  # self.testOut)
        self.root.bind("<c>", self.keyCenter)  # self.testOut)
        self.root.bind("<d>", self.keyD)  # self.testOut)
        self.root.bind("<t>", self.keyT_test)  # self.testOut)

        self.root.bind("<i>", self.key_zi)  # self.testOut)
        self.root.bind("<o>", self.key_zo)  # self.testOut)

        # Binding dell'evento movimento del mouse
        self.root.bind("<Motion>", self.aggiorna_coordinata)

        self.label.bind("<Button-3>", self.button_3_on_click)
        self.label.bind("<Button-2>", self.button_2_on_click)
        self.label.bind("<Button-1>", self.label_on_click)
        self.label.bind("<ButtonRelease-1>", self.label_off_click)
        self.label.bind("<Motion>", self.label_motion_click)

        # Bind dell'evento "<Configure>" alla finestra principale
        self.root.bind("<Configure>", self.on_configure)

        self.update_value()

        # a = CL_mandelbrot(self)
        self.keyM(None)

        # self.Fmbut1 = False
        # self.Fmbut2 = False
        # self.Fmbut3 = False
        self.FdrawRadius = 0

    def keyT_test(self, event):
        cx, cy, rd = self.oFrame1.getData()
        self.MandelCxP,self.MandelCyP,self.MandelRadius = float(cx),float(cy),float(rd)
        print(cx, cy, rd)

    def checkbox_selection(self):
        dati.CLdati.var1 = self.var1.get()
        print(f'var1:{self.var1.get()}')
        self.keyM(0)

    # ottiene posizione e dimensione finestra

    def on_configure(self, event):
        # print(event)
        pass

    bn = 0

    def on_button_click(self):
        self.bn += 1
        self.button.config(text=f"Hai premuto il pulsante! {self.bn} volte")
        # test4.test4(self)
        print("qui 002a")

        w, h = self.width, self.height  # = 1600, 1600   # 1024, 1024
        cx, cy, rd = self.MandelCxP, self.MandelCyP, self.MandelRadius
        pcx, pcy = self.MandelCx, self.MandelCy

        # 3840, 1920   #12000,12000  #20000, 20000 # 30720,17720 # 15360,8640  # 3840, 1920   # 1024, 1024
        # self.width, self.height = 22000,22000 #  7680,4320
        self.width, self.height = self.widthImg, self.heightImg # = 8000,8000 # 3840,2160#8000,8000 # 3840,2160
        # -0.613766, 0.681183, 0.000000675 # -1.6254037, 0, 0.027 # -0.75,0,1.5 # -1.19, 0.282 , 0.0796874
        # self.MandelCxP, self.MandelCyP, self.MandelRadius = -0.50, 0, 1.5
        self.MandelCxP, self.MandelCyP, self.MandelRadius = self.oFrame1.getData()

        # dati.CLdati.var1 = 1
        # self.var1 = 1

        # da qui calcola l'immaginr da salvare 

        self.keyM(None)


        self.image.save("immagine.png")
        # Converte l'immagine in RGB
        image_rgb = self.image.convert("RGB")
        # Salva l'immagine come JPEG
        image_rgb.save("immagine_rgb.jpg", "JPEG")        

        print("qui 002b")

        self.width, self.height = w, h
        self.MandelCxP, self.MandelCyP, self.MandelRadius = cx, cy, rd
        self.MandelCx, self.MandelCy = pcx, pcy

        self.keyM(None)

        print("qui 002c")

    FDrag = False
    cx1, cy1, cx2, cy2 = 0, 0, 0, 0
    dist = 1
    newRadius = 1
    Fmotion = False
    Fpressed = False

    def e1cmd(self, event):
        widget = event.widget
        s = widget.get()
        print(s)
        widget.delete(0, tk.END)
        widget.insert(0, "")
        print("qui1 002", event)

    def keyCenter(self, event):
        self.MandelCxP = -0.5
        self.MandelCyP = 0
        self.MandelRadius = 1.5
        self.cx1 = self.width/2
        self.cy1 = self.height/2
        self.distRadius = min(self.width, self.height)/2
        self.cx2 = self.cx1 + self.distRadius
        self.cy2 = self.cy1 + self.distRadius

    def button_2_on_click(self, event):
        print(event, event.num)

        # Mandel.prova_mandel(self)
        # self.mandelbrot_cpu_2()

    def button_3_on_click(self, event):
        self.FdrawRadius = not self.FdrawRadius
        print(event, event.num, self.FdrawRadius)
        print(f'self.FdrawRadius: {self.FdrawRadius}')

        # Mandel.prova_mandel(self)
        # self.mandelbrot_cpu_2()

    def label_on_click(self, event):
        print(event, event.num)
        self.cx1, self.cy1 = event.x, event.y
        self.MandelCxP = (self.cx1 - self.width/2) / \
            (self.width/2) * self.MandelRadius + self.MandelCx
        self.MandelCyP = (self.cy1 - self.height/2) / \
            (self.height/2) * self.MandelRadius + self.MandelCy
        # self.cx1 -= self.width/2
        # self.cy1 -= self.height/2
        print(self.cx1, self.cy1, event.x, event.y)
        # print("click on")
        self.Fpressed = True

    def label_off_click(self, event):
        print(event)
        self.cx2, self.cy2 = event.x, event.y
        # self.cx2 -= self.width/2
        # self.cy2 -= self.height/2

        # print(self.cx2, self.cy2,event.x, event.y)

        dx = self.cx2-self.cx1
        dy = self.cy2-self.cy1
        dist = math.sqrt(dx*dx+dy*dy)

        if dist >= 10:
            self.dist = dist

        self.distRadius = self.dist

        # if self.dist > 10:
        #     self.MandelRadius = (self.dist / min(self.width,self.height))
        #     pass
        # print(f'dist:{self.dist:4f}')

        # nuovo_centroX = self.RD

        # self.image = Mandel.drawCerchio(self, self.cx1, self.cy1, self.dist)
        # self.image = Image.fromarray(self.image.astype('uint32'), 'RGBA')
        # self.imageSaved = self.image
        self.Fmotion = False
        self.Fpressed = False
        # print("click off")

    def key_zi(self, event):
        # print(f'dist:{self.dist}')
        if self.dist > 10:
            self.MandelRadius = (2*self.MandelRadius) * \
                (self.dist / min(self.width, self.height))
        # self.cx1 = self.width/2
        # self.cy1 = self.height/2
        # self.distRadius = min(self.width, self.height)/2
        # self.cx2 = self.cx1 + self.distRadius
        # self.cy2 = self.cy1 + self.distRadius

    def key_zo(self, event):
        # print(f'dist:{self.dist}')
        if self.dist > 10:
            self.MandelRadius = (2*self.MandelRadius) * \
                (1 - (self.dist / min(self.width, self.height)))
        # self.cx1 = self.width/2
        # self.cy1 = self.height/2
        # self.distRadius = min(self.width, self.height)/2
        # self.cx2 = self.cx1 + self.distRadius
        # self.cy2 = self.cy1 + self.distRadius

    def keyM(self, event):
        self.MandelCx = self.MandelCxP
        self.MandelCy = self.MandelCyP
        # self.MandelRadius = self.MandelRadiusP


        v  = self.oFrame1.horizontal_slider.get()
        print(f'horizontal slider: {v}')
        Mandel.pippolo[3] = v # self.oFrame1.horizontal_slider.get()
        print(f'horizontal slider: {Mandel.pippolo[3]}')

        self.image = self.a.Mandelbrot(
            self.width, self.height, self.mouseX, self.mouseY)
        


        self.imageSaved = self.image
        # Da immagine PIL a immagine Tk
        self.tk_image = ImageTk.PhotoImage(self.image)
        # Aggiorna la Label con la nuova immagine
        self.label.config(image=self.tk_image)
        # Mantieni un riferimento alla nuova immagine
        self.label.image = self.tk_image

        # provo
        self.cx1 = self.width/2
        self.cy1 = self.height/2
        # self.distRadius /= (self.distRadius / min(self.width, self.height))
        self.cx2 = self.cx1 + self.distRadius
        self.cy2 = self.cy1 + self.distRadius
        # ----------

    def label_motion_click(self, event):
        # print(event,event.num)
        self.cx2, self.cy2 = event.x, event.y
        if self.Fpressed == True:
            self.Fmotion = True
        # dx = self.cx2-self.cx1
        # dy = self.cy2-self.cy1
        # self.dist = math.sqrt(dx*dx+dy*dy)
        # print(f'dist:{self.dist:4f}')
        # self.image = Mandel.drawCerchio(self,self.cx1,self.cy1,self.dist)
        # self.image = Image.fromarray(self.image.astype('uint32'), 'RGBA')
        # self.imageSaved = self.image           # print(self.cx2, self.cy2,event.x, event.y)
        # print(event)
        # print("click motion")
        pass

    # --- Funzione di aggiornamento

# region UPDATE

    def update_value(self):

        self.mandelbrot_cpu_2()

        self.label.config(anchor="c",
                          text=f"cx:{self.MandelCy:+.18f} cy:{self.MandelCy:+.18f} rd:{self.MandelRadius:.18f}")

        # self.background_label.config(
        #     # compound='center',

        #     text=f"label back: {
        #         self.counter}", font=("Courier", 34),
        #     image=self.tk_image_6,
        # )

        # self.counter += 1  # Aggiorna il valore
        # Aggiorna il testo della label
        # self.label2.config(text=f"Valore: {self.counter}")
        # Richiama la funzione ogni 16 ms
        self.root.after(16, self.update_value)
        # print(self.counter)
        # Cambia l'immagine dell'elemento esistente
        # self.canvas.itemconfig(self.image_id, image=self.tk_image, anchor="sw")

        px = (self.mouseX - self.width/2) / (self.width/2) * \
            self.MandelRadius + self.MandelCx
        py = (self.mouseY - self.height/2) / (self.height/2) * \
            self.MandelRadius + self.MandelCy

        zx, zy = px, py
        c = zx + 1j * zy
        z = 0.0j
        n = 0
        max_radius = 200
        max_iter = 1000
        dist = 100
        zin = dist
        self.array8Cnt = 0
        kn = self.array8.size
        # self.array8 = np.zeros(kn,dtype='complex128')
        # self.array8 = np.full(kn,complex(self.MandelCx,self.MandelCy))
        self.array8 = np.full(kn, c)
        # zinMin = zin
        while abs(z) <= max_radius and n < max_iter:
            z = z*z + c
            n += 1
            dist = abs(z-c)
            if dist < self.MandelRadius and dist > 0:
                self.array8Cnt += 1
                if self.array8Cnt < (self.array8.size):
                    self.array8 = np.roll(self.array8, 1)
                    self.array8[0] = z
        # self.array8[self.array8.size-1] = complex(px,py)

        dist = max(dist, 1e-15)
        v = abs(math.log(abs(dist), 10))
        k = 8
        v = v / k


#         self.label.config(compound='center',
#         text=f"cx:{\
# self.MandelCy:+.18f}\n\
# cy:{self.MandelCy:+.18f}\n\
# rd:{self.MandelRadius:.18f}")

        self.label4.config(anchor="w",
                           text=f"X:{px:+.18f}  Y:{py:+.18f}  n:{n:4.0f}\n \
       dist:{dist:.18f} rd:{self.MandelRadius:.18f}\n  \
       log(dist):{math.log(dist, 10):.18f} /8:{v:.18f}")

        self.label3.config(text=f'{dati.CLdati.var2[0]}')

        # self.image = Mandel.drawArray (self, array, self.MandelCx, self.MandelCy, self.MandelRadius)
        # self.image = Image.fromarray(self.image.astype('uint32'), 'RGBA')
        # self.imageSaved = self.image

        # n:{n:4.0f}    z:{z.real:+8.12f}+j{z.imag:+8.12f}   d:{abs(z):+8.12f} \
        # v:{math.log(abs(z)/math.log(10)):+8.12f} \
        # ")
# endregion

    def testOut(self, event):
        print("qui003")
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        print(f"Posizione finestra - X: {x}, Y: {y}")
        testOut(self, event)

    # --- Funzione per uscire
    def quit(self, event):
        self.root.destroy()
        print("--uscita--")

    def draw(self):
        # Disegno con Cairo
        self.context.set_source_rgb(.1, .3, .2)  # Sfondo
        self.context.paint()
        self.context.set_source_rgb(1, 0, 0)  # Colore rosso
        self.context.arc(self.width / 2, self.height / 2,
                         50, 0, 2 / 3 * 3.14159)
        self.context.fill()
        pass

    # --- movimento cursore
    def setMxy(self, x, y):
        # global mouseX, mouseY
        self.mouseX, self.mouseY = x, y

    def aggiorna_coordinata1(self):
        x, y = self.mouseX, self.mouseY
        # Cancella il contenuto corrente dell'Entry
        self.entry.delete(0, tk.END)
        # rv = ((x * y) % self.RADICE) / self.RADICE
        # pf, pi = math.modf(rv * 10)
        # self.entry.insert(0, f"X: {x:4d}, Y: {y:4d} x*y:{x*y:7d}  R:{self.RADICE:4d} %R /R:{((x*y) % self.RADICE) /
        #                   self.RADICE:1.6f}, rv: {rv:.4f} (pi:{int(pi)}   pf:{pf:.3f})")  # Inserisce le nuove coordinate
        # Inserisce le nuove coordinate
        self.entry.insert(0, f"X: {x:4d}, Y: {y:4d}")

    def aggiorna_coordinata(self, event):
        self.setMxy(event.x, event.y)
        self.aggiorna_coordinata1()
        pass

    def keyA(self, event):
        self.image = draw_R(self.width, self.height)
        self.image = Image.fromarray(self.image.astype('uint32'), 'RGBA')
        self.imageSaved = self.image
        # Da immagine PIL a immagine Tk
        self.tk_image = ImageTk.PhotoImage(self.image)
        # Aggiorna la Label con la nuova immagine
        self.label.config(image=self.tk_image)
        # Mantieni un riferimento alla nuova immagine
        self.label.image = self.tk_image

    def keyC(self, event):
        print(event)
        self.mandelbrot_cpu_2()

    def keyD(self, event):
        self.image = self.imageSaved
        self.mandelbrot_cpu_2()

    def mandelbrot_cpu_2(self):


        if not Mandel.testInLabel(self):
            return

        image1 = Mandel.prova_mandel(self)

        self.image = Image.fromarray(image1.astype('uint32'), 'RGBA')
        # Da immagine PIL a immagine Tk
        self.tk_image = ImageTk.PhotoImage(self.image)
        # Aggiorna la Label con la nuova immagine
        self.label.config(image=self.tk_image)
        # Mantieni un riferimento alla nuova immagine
        self.label.image = self.tk_image

        pass

    def run(self):
        # Avvia il ciclo principale di Tkinter
        self.root.mainloop()
# endregion ---------------------------------------------------------------------------------------------------


# region CL_mandelbrot

class CL_mandelbrot():

    def __init__(self, ist):
        self.ist = ist
        pass

    def Mandelbrot(self, w, h, mx, my):

        # print(f'w:{w} h:{h}  mx:{mx}  my:{my}')

        # width1, height1 = 4000, 4000
        # max_iter = 100  # Numero massimo di iterazioni
        # x_min, x_max = -2.0, 1.0  # Limiti dell'asse X
        # y_min, y_max = -1.5, 1.5  # Limiti dell'asse Y

        # image1 = Mandel.mandelbrot_cpu(x_min, x_max, y_min,
        #                                y_max, width1, height1, max_iter)

        cx = self.ist.MandelCx
        cy = self.ist.MandelCy
        rd = self.ist.MandelRadius



        w = self.ist.width - 0
        h = self.ist.height - 0
        

        print("qui4444444441234")    

        n = 1000
        # rd = 0.01
        # cx = -1.5
        # cy = 0


        t1 = time.time()
        image1 = Mandel.mandelbrot_cxcyrd(cx, cy, rd, w, h, n)
        # image1 = np.zeros((self.ist.height, self.ist.width), dtype=np.uint32)
        t2 = time.time()
        print(t2-t1, "sec")

        # questa non và, deve prendere da una immagine .png
        # image1 = np.array(image1.resize(400,400).convert("RGBA"))

        # image_pil = Image.fromarray(image1.astype('uint32'), 'RGBA')
        image_pil = Image.fromarray(image1.astype('uint32'), 'RGBA')
        # image_pil = image_pil.resize((1000,1000))

        # image_pil = image_pil.filter(ImageFilter.CONTOUR)  # Raggio 5

        return image_pil
# endregion


# region draw_R

@jit(nopython=True, parallel=True, nogil=True, cache=True)
def draw_R(width, height):

    print("draw_R")

    RADICE = 800
    rd = 1
    di = rd - .4
    STP = 10

    ymax = height  # RADICE
    xmax = width  # RADICE
    count = 0

    image1 = np.zeros((height, width), dtype=np.uint32)

    c = np.array([0, 0, 0], dtype='uint32')

    # print('--start--')

    for y in range(ymax):

        for x in range(xmax):

            count += 1

            rv = ((x*y) % RADICE)/RADICE

            # c = colorsys.hsv_to_rgb(0.25/6, 1, 1) # rv)
            c = np.array([50, 255, 100], dtype='uint32')

            # pf,pi = math.modf(rv * STP)
            pi = int(rv * STP)
            pf = rv - pi

            if pi == 0:
                rv *= 12
                # c = colorsys.hsv_to_rgb(rv, 1, 1)
                c[0] = 0
                c[1] = 20
                c[2] = 200
                # di =8 / 10 * rd
            else:
                # c = (.5,1,.05)
                # di = 2 / 10 * rd
                if int(pf*100) != 0:
                    # c[:] = [0, 0, 0]
                    c[0] = 0
                    c[1] = 0
                    c[2] = 00
                    # di = 1 / 10 * rd
                else:
                    # c[:] = [201, 201, 201]
                    c[0] = 201
                    c[1] = 201
                    c[2] = 201
                    # di = 1 / 10 * rd

            color = c[0] | c[1] << 8 | c[2] << 16 | 0x0ff000000

            image1[y, x] = color

    # print('--stop--')
    # image2 = Image.fromarray(image1.astype('uint32'), 'RGBA')

    return image1

# endregion


def testOut(self, event):
    print("qui testOut", self.xyz, event)
    pass


if __name__ == "__main__":

    os.system('clear')
    a = CL_App1(tk.Tk())
    a.run()
