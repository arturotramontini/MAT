import dati
import time
import tkinter as tk
import numpy as np


class CLdati:
    var1 = 0
    var2 = np.zeros(1, dtype=np.int32)


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        # Bind degli eventi
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tip_window or not self.text:
            return

        # Creazione della finestra del tooltip
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Nessun bordo/finestra
        tw.wm_geometry(f"+{x}+{y}")

        # Inserimento del testo
        label = tk.Label(tw, text=self.text, background="yellow",
                         relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack(ipadx=5, ipady=3)

    def hide_tooltip(self, event):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class CLframe2:

    def __init__(self, ist, root):

        self.ist = ist
        self.root = root
        print(self.ist.xyz)
        self.labelframe = tk.Frame(self.ist.fr0,  padx=4, pady=4, bg="blue")
        self.labelframe.pack(padx=5, pady=5, side=tk.LEFT)
        self.labelframe.bind('<Leave>', self.rimuovi_focus)


        # self.labelframe
        self.fr1 = tk.Frame(self.labelframe)
        self.entryRD = tk.Entry(self.fr1, font=(
            "Unifont", 12),  width=40)  # 100)
        self.entryRD.insert(0, "1.2")
        self.entryRD.pack(padx=4, pady=4, side="right")
        dati.Tooltip(self.entryRD, "Radius,cx,cy")
        self.l1 = tk.Label(self.fr1, text="rd,cx,cy", font=(
            "Courier", 12)).pack(padx=0, pady=0, side="left")
        self.fr1.pack()
        
        # button 1 -
        # , from_=0, to=100, orient=tk.HORIZONTAL)
        self.button1 = tk.Button(self.labelframe, text='get')
        self.button1.pack(anchor='e',side=tk.LEFT, padx=4,pady=4)
        self.button1.bind('<ButtonPress>', self.button1_press)
        
        # button 2 -
        # , from_=0, to=100, orient=tk.HORIZONTAL)
        self.button2 = tk.Button(self.labelframe, text='set')
        self.button2.pack(anchor='e',side=tk.LEFT, padx=4,pady=4)
        self.button2.bind('<ButtonPress>', self.button2_press)

    def button1_press(self, event):
        print(event, "Frame2 Button1 pressed")
        s = str(self.ist.MandelRadius) +', '
        s += str( self.ist.MandelCxP) + ', '
        s += str(self.ist.MandelCyP)
        self.entryRD.delete(0, 'end')
        self.entryRD.insert(0, s)        
        print(s)

    def button2_press(self, event):
        print(event, "Frame2 Button2 pressed")
        s = self.entryRD.get()+"0,0,0"
        p=(s.split(","))
        print(p)
        n = np.array([float(x) for x in s.split(",")], dtype=np.float64)
        self.ist.MandelRadius, self.ist.MandelCxP, self.ist.MandelCyP = n[0], n[1], n[2]
        print(n.tolist())




    def rimuovi_focus(self, event):
        self.root.focus()

class CLframe1:

    def __init__(self, ist, root):

        self.ist = ist
        self.root = root
        print(self.ist.xyz)

        # self.labelframe = tk.LabelFrame(self.root, text="Sezione Raggruppata", padx=10, pady=10,bg="red")
        # self.labelframe = tk.LabelFrame(self.ist.fr0, text="Sezione Raggruppata", padx=10, pady=10,bg="red")
        self.labelframe = tk.Frame(self.ist.fr0,  padx=10, pady=10, bg="red")
        # ,width=200,height=100) #side="right")# side="top",fill="none")#
        self.labelframe.pack(padx=5, pady=5, side="bottom", anchor="w")

        self.labelframe.bind('<Leave>', self.rimuovi_focus)

        # tk.Label(self.labelframe, text="rd").grid(row=0,column=0)#side="left")

        self.fr1 = tk.Frame(self.labelframe)
        self.entryRD = tk.Entry(self.fr1, font=(
            "Unifont", 12),  width=20)  # 100)
        self.entryRD.insert(0, "1.2")
        self.entryRD.pack(padx=4, pady=4, side="right")
        # self.entryRD.grid(row=0, column=1)
        self.entryRD.bind('<KP_Enter>', self.e1cmdRadius)
        # self.entryRD.bind('<Leave>', self.rimuovi_focus)
        # self.entryRD.bind('<Enter>', self.rimuovi_focus)
        dati.Tooltip(self.entryRD, "Radius")
        self.l1 = tk.Label(self.fr1, text="rd", font=(
            "Courier", 12)).pack(padx=0, pady=0, side="left")
        self.fr1.pack()

        self.fr2 = tk.Frame(self.labelframe)
        self.entryCX = tk.Entry(self.fr2, font=(
            "Unifont", 12),  width=20)  # 100)
        self.entryCX.insert(0, "-0.75")
        self.entryCX.pack(padx=4, pady=4, side="right")
        # self.entryCX.bind('<KP_Enter>', self.e1cmdCX)
        # self.entryCX.bind("<Leave>", self.rimuovi_focus)
        dati.Tooltip(self.entryCX, "CX")

        self.l2 = tk.Label(self.fr2, text="cx", font=(
            "Courier", 12)).pack(side="left")
        self.fr2.pack()

        self.fr3 = tk.Frame(self.labelframe)
        self.entryCY = tk.Entry(self.fr3, font=(
            "Unifont", 12),  width=20)  # 100)
        self.entryCY.insert(0, "0.0")
        self.entryCY.pack(padx=4, pady=4, side="right")
        self.entryCY.bind('<KP_Enter>', self.e1cmdCY)
        # self.entryCY.bind('<Leave>', self.rimuovi_focus)
        dati.Tooltip(self.entryCY, "CY")
        self.l3 = tk.Label(self.fr3, text="cy", font=(
            "Courier", 12)).pack(side="right")
        self.fr3.pack()

        # Slider orizzontale
        self.horizontal_slider = tk.Scale(
            self.labelframe, from_=0, to=100, orient=tk.HORIZONTAL)
        self.horizontal_slider.set(43)
        self.horizontal_slider.pack(fill='both')
        self.horizontal_slider.bind('<B1-Motion>', self.slider_motion)

        # button 2 -
        # , from_=0, to=100, orient=tk.HORIZONTAL)
        self.button2 = tk.Button(self.labelframe, text='get')
        self.button2.pack(fill='both')
        self.button2.bind('<ButtonPress>', self.button2_press)

    def rimuovi_focus(self, event):
        print(event)
        self.horizontal_slider.focus_set()
        self.root.focus()
        print('focus rimosso')

    def getData(self):
        return float(self.entryCX.get()), float(self.entryCY.get()), float(self.entryRD.get())

    def button2_press(self, event):
        print(event, "Button2 pressed")
        cx = self.ist.MandelCx
        rd = self.ist.MandelRadius
        cy = self.ist.MandelCy
        self.entryCX.delete(0, 'end')
        self.entryCX.insert(0, str(cx))
        self.entryCY.delete(0, 'end')
        self.entryCY.insert(0, str(cy))
        self.entryRD.delete(0, 'end')
        self.entryRD.insert(0, str(rd))

    def slider_motion(self, event):
        print("x123", event, self.horizontal_slider.get())
        pass

    def e1cmdRadius(self, event):
        print("qui191 Radius", event, float(self.entryRD.get()))
        print(self.ist.xyz)
        self.ist.xyz = 0.3456

    def e1cmdCX(self, event):
        print("qui191 CX", event)

    def e1cmdCY(self, event):
        print("qui191 CY", event)


def monitor_progress(progress, interval=0.2):
    """Monitora l'avanzamento"""
    cnt = 0
    while progress[0] < 99.0:
        cnt += 1
        print(f"Avanzamento: {progress[0]:.2f}%  {cnt}", end='\r')
        time.sleep(interval)
    print(f"\nAvanzamento finale: {progress[0]:.2f}%  {cnt}", end='\n')
    time.sleep(0.5)
    print("Operazione completata!\n")
