import math
import cmath

# from numba import njit
# from numba import jit, prange


USE_JIT = True

if USE_JIT:
    from numba import jit
    from numba import njit
    from numba import prange
else:
    def jit(func):
        return func  # Decoratore "neutro"




import numpy as np

from matplotlib.colors import hsv_to_rgb
import matplotlib



def rgb_to_hsv(r, g, b):
    # Normalizza i valori RGB (se non lo sono già)
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # Calcola C_max, C_min e delta
    C_max = max(r, g, b)
    C_min = min(r, g, b)
    delta = C_max - C_min

    # Calcolo della tonalità (H)
    if delta == 0:
        H = 0
    elif C_max == r:
        H = (60 * ((g - b) / delta) + 360) % 360
    elif C_max == g:
        H = (60 * ((b - r) / delta) + 120) % 360
    elif C_max == b:
        H = (60 * ((r - g) / delta) + 240) % 360

    # Calcolo della saturazione (S)
    S = 0 if C_max == 0 else (delta / C_max)

    # Calcolo del valore (V)
    V = C_max

    return H, S, V

# # Esempio d'uso
# h, s, v = rgb_to_hsv(255, 0, 0)  # Rosso puro
# print(f"H: {h}, S: {s}, V: {v}")

@njit
def hsv_to_rgb_1(h, s, v):
    h = h % 360
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r = (r + m)
    g = (g + m)
    b = (b + m)

    if math.isnan(b):
        print("ferma_qui", b)
        b = 0


    return r, g, b

    # Esempio d'uso
    r, g, b = hsv_to_rgb(120, 1, 1)  # Verde puro
    print(f"R: {r}, G: {g}, B: {b}")



# @jit
# def clamp(value, min_value, max_value):
# 	return max(min_value, min(max_value, value))
# @jit
# def saturate(value):
# 	return clamp(value, 0.0, 1.0)
# @jit
# def hue_to_rgb(h):
# 	r = abs(h * 6.0 - 3.0) - 1.0
# 	g = 2.0 - abs(h * 6.0 - 2.0)
# 	b = 2.0 - abs(h * 6.0 - 4.0)
# 	return saturate(r), saturate(g), saturate(b)
# @jit
# def hsl_to_rgb(h, s, l):
# 	r, g, b = hue_to_rgb(h)
# 	c = (1.0 - abs(2.0 * l - 1.0)) * s
# 	r = (r - 0.5) * c + l
# 	g = (g - 0.5) * c + l
# 	b = (b - 0.5) * c + l
# 	return r, g, b

@jit
def hsl_to_hsv(h, s_hsl, l):
    v = l + s_hsl * min(l, 1 - l)
    s_hsv = 0 if v == 0 else 2 * (1 - l / v)
    return h, s_hsv, v

@jit
def hsv_to_hsl(h, s_hsv, v):
    l = v * (1 - s_hsv / 2)
    s_hsl = 0 if l in [0, 1] else (v - l) / min(l, 1 - l)
    return h, s_hsl, l



@jit
def hsv_to_rgb_2(h, s, v):
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]

    return r, g, b

import dati
from dati import CLdati

import threading

import Mandel

pippolo = np.zeros(4,dtype=np.float64) 


def mandelbrot_cxcyrd(cx,cy,rd,w,h,n):

    # global pippolo

    # pippolo[0] = 35 #pippolo[1]  # 456.3
    # pippolo[1] = 35.11 #pippolo[1]  # 456.3
    # pippolo[2] = 35.22 #pippolo[1]  # 456.3
    # # pippolo[3] = 35.33 #pippolo[1]  # 456.3
    # n111  = Mandel.pippolo[3] + 17
    # Mandel.pippolo[3] = n111
    # print(f'horizontal slider in Mandel [3]: ',Mandel.pippolo[3], n111)

    Lmin = min(w,h)
    Lmax = max(w,h)
    step = rd / (Lmin / 2)

    # if w >= h :
    #     t = Lmin
    #     Lmin = Lmax
    #     Lmax = t
    
    # x_min = cx - step * Lmin / 2
    # x_max = cx + step * Lmin / 2
    # y_min = cy - step * Lmax / 2
    # y_max = cy + step * Lmax / 2    
    
    x_min = cx - step * w / 2
    x_max = cx + step * w / 2
    y_min = cy - step * h / 2
    y_max = cy + step * h / 2
    
    # Creazione dell'array al di fuori della funzione
    # array_complessi = np.zeros(8, dtype=np.complex128)


    dati.CLdati.var2[0] = 0
    progress = dati.CLdati.var2
    monitor_thread = threading.Thread(target=dati.monitor_progress, args=(progress,))
    monitor_thread.start()
    



    var1 = dati.CLdati.var1
    var2 = dati.CLdati.var2

   
    # image = mandelbrot_cpu(x_min, x_max, y_min, y_max, w,h, n, array_complessi)
    arcioppi, image = mandelbrot_cpu(rd, x_min, x_max, y_min, y_max, w,h, n,var1, var2,pippolo)


    # print(f'horizontal slider in Mandel [3] ritorno: ',pippolo[3], n111)

    print (f"variabile: ",  arcioppi[0], "  --stop 2-- \n")

    return image
    pass




# # region calcolo mandelbrot
@njit(nopython=True, parallel=True, nogil=True, cache=True)
# @jit # (nogil=True, cache=True) # nopython=True, parallel=True, nogil=True, cache=True)
# def mandelbrot_cpu(x_min, x_max, y_min, y_max, width, height, max_iter, array):
# @njit
def mandelbrot_cpu(rd, x_min, x_max, y_min, y_max, width, height, max_iter, var1, var2,pippolo1):
    

    print("qui555555", width, height, "  -   ")

    # global pippolo  # Usa il nome globale

    # var2 = 0 # setta la percentuale di avanzamento

    # print(f'var1...:{var1}')

    # n111 = pippolo[0]
    # print(f'horizontal slider in mandelbrot_cpu: ', pippolo1[0])
    # print(f'horizontal slider in mandelbrot_cpu: ', pippolo1[1])
    # print(f'horizontal slider in mandelbrot_cpu: ', pippolo1[2])
    # print(f'horizontal slider in mandelbrot_cpu 3a: ', pippolo1[3])
     

    w = width
    w2 = w/2
    h = height
    h2 = h/2

    image = np.zeros((height, width), dtype=np.uint32)

    iter = 10 # 256
    tx = np.linspace(1, iter, iter)
    ty1 = np.sin(tx/iter*2*math.pi*3+0.0)*250
    ty2 = np.sin(tx/iter*2*math.pi*27+0.0)*250
    ty3 = np.sin(tx/iter*2*math.pi*31+0.0)*250

    max_radius = 100.0

    # for y in prange(height):
    for y in range(height):

        for x in range(width):

            # ------------
            p = ((x+y*width)/(width*height))
            var2[0] = int(100 * p)
            # ------------

            zx, zy = x * (x_max - x_min) / width + x_min, y * \
                (y_max - y_min) / height + y_min
            c = zx + 1j * zy
            z = 0.0j
            iter = 0

            zprev = z
            zin = 1e-3

            dist = (z * zprev.conjugate()).real
            r2 = max_radius * max_radius

            # modo che funziona abbastanza
            while dist < r2 and iter < max_iter:
                z = z*z + c
                iter += 1
                dist = (z * z.conjugate()).real
                if dist < rd and dist > 0:
                    zin = dist

            L1 = abs( math.log(dist) / math.log(max_radius) ) # smooth
            L2 = math.log(L1) / math.log(2) # smoother

            fractIter =  L2 - 0

            iterF = iter - fractIter # transizioni sfumate

            v = math.sqrt(iterF/max_iter) # *360

            r,g,b = hsv_to_rgb_2(v,1,1)
            r, g, b = [int(xv * 255) for xv in (r, g, b)]

            color = (b << 16) | (g << 8) | (r << 0) | 0x0ff000000

            # se  parte interna
            if iter >= max_iter  :

                v = abs(math.log10(abs(zin-0 )))


                k = 8
                v = v / k  
                v = abs(math.log10(v)/math.log10(3.0))


                r,g,b = hsv_to_rgb_2(v,1,1)


                b *= .3

                r,g,b = [int(xv * 255) for xv in (r, g, b)]


                color = (g << 16) | (r << 8) | (b << 0) | 0x0ff000000

                # ABGR
                color &= 0x0ffffffff                

            if var1 != 0:
                color = color ^ 0x00ffff00
            image[y, x] = color


    cioppi = np.zeros(2,dtype=np.float64)
    cioppi [0] = 1234.5678

    return cioppi, image

# endregion


def assi(image):
    w,h = np.shape(image)
    color = 0x0ffffffff
    for x in range(w):
        image[int(h/2),x] = color
    for y in range(h):
        image[y,int(w/2)] = color

def riga(image,x1,y1,x2,y2):
    # print(f'x1:{x1:4f},y1:{y1:4f},  x2:{x2:4f},y2:{y2:4f},  {np.shape(image)}')

    w,h = np.shape(image)

    # -------- disegna linea -----------


    x1 += w/2
    x2 += w/2

    y1 += h/2
    y2 += h/2

    # y1 = h/2 - y1
    # y2 = h/2 - y2

    #------------

    x1 = min(max(1,x1), (w-2))
    x2 = min(max(1,x2), (w-2))
    y1 = min(max(1,y1), (h-2))
    y2 = min(max(1,y2), (h-2))

    #------------


    dx = x2-x1 
    dy = y2-y1
    ratio = 0
    sign = 1
    x = 0
    y = 0

    color = 0x0ffffffff
    color2 = 0x02f9f9f9f

    if abs(dx) >= abs(dy):
        if dx != 0: ratio = (dy / dx)
        if dx < 0 : sign = -1
        for n in range(int(abs(dx))):
            x = int(x1 + sign * n)
            y = int(y1 + sign * n * ratio)
            image[y,x] = color
            # image[y,x-1] = color2
            # image[y,x+1] = color2
            # image[y-1,x] = color2
            # image[y+1,x] = color2
            
    if abs(dy) > abs(dx):        
        if dy != 0: ratio = (dx / dy)
        if dy < 0 : sign = -1
        for n in range(int(abs(dy))):
            x = int(x1 + sign * n * ratio)
            y = int(y1 + sign * n )
            image[y,x] = color
            # image[y,x-1] = color2
            # image[y,x+1] = color2
            # image[y-1,x] = color2
            # image[y+1,x] = color2
    # --------------------------------
    pass


# def drawArray(ist,array,xc,yc,rd):
#     image = ist.imageSaved
#     shp = np.shape(image)
#     # print(shp)
#     w=shp[0]
#     h=shp[1]
#     array_uint8 = np.array(image) 
#     # Conversione in uint32 combinando i 4 canali
#     image = (array_uint8[..., 3].astype("uint32") << 24) | \
#                    (array_uint8[..., 2].astype("uint32") << 16) | \
#                    (array_uint8[..., 1].astype("uint32") << 8) | \
#                    (array_uint8[..., 0].astype("uint32"))

#     for i in range (array.size-1):
#         # print(array[i])
#         x1 = ((array[i].real - xc) / rd) * (w/2)
#         y1 = ((array[i].imag - yc) / rd) * (h/2)
#         x2 = ((array[i+1].real - xc) / rd) * (w/2)
#         y2 = ((array[i+1].imag - yc) / rd) * (h/2)
#         # riga(image,0,0,100,200) # x1,y1,x2,y2)
#     # return image      

def cerchio(image,xc,yc,rd):
    w,h = np.shape(image)
    xc -= w/2
    yc -= h/2
    rd = max(4,rd)
    stepAngolo = 5
    for angolo in range (0 ,360, stepAngolo):
        x1 = xc + rd * math.cos(math.radians(angolo))
        y1 = yc + rd * math.sin(math.radians(angolo))
        a = angolo + stepAngolo
        x2 = xc + rd * math.cos(math.radians(a))
        y2 = yc + rd * math.sin(math.radians(a))
        riga(image,x1,y1,x2,y2)
        pass
    pass




def drawCerchio(ist,xc,yc,rd):
    image = ist.imageSaved
    shp = np.shape(image)
    # print(shp)
    w=shp[0]
    h=shp[1]
    array_uint8 = np.array(image) 
    # Conversione in uint32 combinando i 4 canali
    image = (array_uint8[..., 3].astype("uint32") << 24) | \
                   (array_uint8[..., 2].astype("uint32") << 16) | \
                   (array_uint8[..., 1].astype("uint32") << 8) | \
                   (array_uint8[..., 0].astype("uint32"))
    xc -= w/2
    yc -= h/2
    stepAngolo = 5
    
    rd = max(4,rd)
    stepAngolo = max(5,int(math.degrees(math.asin(2/rd))))
    print(stepAngolo)

    for angolo in range (0 ,360, stepAngolo):
        x1 = xc + rd * math.cos(math.radians(angolo))
        y1 = yc + rd * math.sin(math.radians(angolo))
        a = angolo + stepAngolo
        x2 = xc + rd * math.cos(math.radians(a))
        y2 = yc + rd * math.sin(math.radians(a))
        riga(image,x1,y1,x2,y2)
    return image









def testInLabel(ist):
    # Ottieni la posizione del mouse relativa alla finestra
    mouse_x, mouse_y = ist.root.winfo_pointerx(), ist.root.winfo_pointery()
    # print(mouse_x, mouse_y,"2")
    
    # Ottieni la posizione e le dimensioni della label
    label_x = ist.label.winfo_rootx()
    label_y = ist.label.winfo_rooty()
    label_width = ist.label.winfo_width()
    label_height = ist.label.winfo_height()

    Flag = False
    # Verifica se il mouse è dentro i confini della label
    if label_x <= mouse_x <= label_x + label_width and label_y <= mouse_y <= label_y + label_height:
        # print("Mouse è sopra l'immagine")
        Flag = True
    else:
        # print("Mouse è fuori dall'immagine")
        Flag = False
    return Flag


# arc = np.zeros(5,dtype="complex128")

def prova_mandel (ist):


    image = ist.imageSaved
    # image = ist.image




    # print(ist.xyz)
    w = ist.width 
    h = ist.height

    array_uint8 = np.array(image) 

    # print(array_uint8.shape) # np.shape(image))

# Conversione in uint32 combinando i 4 canali
    image = (array_uint8[..., 3].astype("uint32") << 24) | \
                   (array_uint8[..., 2].astype("uint32") << 16) | \
                   (array_uint8[..., 1].astype("uint32") << 8) | \
                   (array_uint8[..., 0].astype("uint32"))

    # image = array_uint8.view(dtype="uint32").reshape((800, 800, 1))
    

    # print(image.shape) # np.shape(image))
    # image = np.zeros((h, w), dtype=np.uint32)
    # image.fill(0x0ff101010)

    # cursore, crocetta 10x10
    x = min(max(ist.mouseX,10),ist.width-10)
    y = min(max(ist.mouseY,10),ist.height-10)
    for iy in range (10):
        image[y+iy-5,x]=0x00ffff0000 # ABGR  
    for ix in range (10):
        image[y,x+ix-5]=0x00ffff0000 # ABGR  



    # # cursore             
    # x = min(ist.mouseX,w-1)
    # y = min(ist.mouseY,h-1)
    # for _ in range (w):
    #     image[y,_]=0x007f00ffff # ABGR
    # for _ in range (h):
    #     image[_,x]=0x007f00ffff # ABGR

    # # assi cartesiani             
    # for _ in range (w):
    #     image[int(h/2),_]=0x007fff00ff # ABGR
    # for _ in range (h):
    #     image[_,int(w/2)]=0x007fff00ff # ABGR

    # print(f'radius:{ist.Radius}, cx:{ist.cx}, cy:{ist.cy}')


    new_cx = 2 * (x / w - 0.5)  * ist.MandelRadius + ist.MandelCx
    new_cy = 2 * (y / h - 0.5)  * ist.MandelRadius + ist.MandelCy
    # print(f'ncx:{new_cx}, ncy:{new_cy}')


    # -------- disegna riga -----------
    # x1 = 0
    # y1 = 0
    # x2 = ist.mouseX - w/2 
    # y2 = ist.mouseY - h/2 
    # riga(image,x1,y1,x2,y2)

    # cerchio(image, ist.mouseX, ist.mouseY, 20)

    if ist.Fmotion == True :
        dx = ist.cx2 - ist.cx1
        dy = ist.cy2 - ist.cy1
        dist = math.sqrt(dx*dx+dy*dy)        
        # cerchio(image, ist.cx1 - w/2, ist.cy1 - h/2, dist)
        cerchio(image, ist.cx1 , ist.cy1 , dist)
    #----------------------------------

    # #--------------- prova disegno righe ---------
    # # a = np.ndarray(5,dtype="complex128")
    # # a = np.zeros(5,dtype="complex128")
    # a = np.zeros(5,dtype="complex128")
    
    # # print("--------------------")
    # # print(a)

    # a[0] =  0 + 0j
    # a[1] =  1 - 1j
    # a[2] = -2 - 2j
    # a[3] = -3 + 3j
    # a[4] =  4 + 4j
    # a = a * 0.0125

    # c = complex(ist.MandelCx, ist.MandelCy)
    # a = a - c # (0.5+0.5j)
    # # print (c)

    # Minw = min(ist.width, ist.height)
    # a = a / (2.0*ist.MandelRadius)
    # a = a * Minw

    # for i in range (a.size-1):
    #     x1 = a[0+i].real
    #     y1 = a[0+i].imag
    #     x2 = a[1+i].real
    #     y2 = a[1+i].imag
    #     riga(image,x1,y1,x2,y2)            
    # #---------------------------------------------





    if ist.FdrawRadius :
        #--------------- prova disegno righe ---------
        a = ist.array8
        c = complex(ist.MandelCx, ist.MandelCy)
        a = a - c

        Minw = min(ist.width, ist.height)

        a = a / (2.0*ist.MandelRadius)
        a = a * Minw

        for i in range (a.size-1):
            x1 = a[0+i].real
            y1 = a[0+i].imag
            x2 = a[1+i].real
            y2 = a[1+i].imag
            riga(image,x1,y1,x2,y2)            
        

    if ist.FdrawRadius :
        # riga(image,10,30,100,300)
        KN = 32
        Cx = ist.cx1 - ist.width/2
        Cy = ist.cy1 - ist.height/2
        Rd = ist.distRadius
        for angolo in range (KN):
            a1 = angolo * (2 * math.pi / KN)
            a2 = (angolo+1) * (2 * math.pi / KN)
            x1 = Cx + Rd * math.cos (a1)
            y1 = Cy + Rd * math.sin (a1)
            x2 = Cx + Rd * math.cos (a2)
            y2 = Cy + Rd * math.sin (a2)
            riga(image,x1,y1,x2,y2)            

        # riga(image,Cx-Rd,Cy,Cx+Rd,Cy)
        # riga(image,Cx,Cy-Rd,Cx,Cy+Rd)
        assi(image)

    #---------------------------------------------









    ist.counter2 += 1
    # Aggiorna il testo della label
    ist.label3.config(text=f"label3: {ist.counter2:6d}")    

    return image
