#----------------------------------------------
# Maturarbeit "Stereograms"
# Nuno Furrer, 2024
#
# v11, 2024/10/10
#----------------------------------------------

import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from random import randrange
import os

base_dir = 'Required Images'
texture_img_path = os.path.join(base_dir, "blue.jpg")
Depthmap_path = os.path.join(base_dir, "torusDepth.png")
Head_image_path = os.path.join(base_dir, "Head.png")

# Miscellaneous functions
def img_to_arr(Depthmap):
    maxX, maxY = Depthmap.width, Depthmap.height
    Z = np.zeros((maxX, maxY))
    for x in range(maxX):
        for y in range(maxY):
            pixval = Depthmap.getpixel((x, y))
            #print(pixval)
            Z[x, y] = pixval/256 #Depthmap.getpixel([x,y])
    return Z

def import_texture_image():
    global texture_img
    file_path = filedialog.askopenfilename()
    if file_path:
        texture_img = Image.open(file_path).convert('RGB')
        update_texture_preview()

def import_depth_image():
    global Depthmap, Z, maxX, maxY
    file_path = filedialog.askopenfilename()
    if file_path:
        Depthmap = Image.open(file_path).convert('L')
        maxX, maxY = Depthmap.width, Depthmap.height
        Z = img_to_arr(Depthmap)
        reset_canvas()
        update_depth_preview()


def reset_canvas():
    global image, tkimg
    image = np.ones((maxY, maxX, 3), dtype=np.uint8)*255
    tkimg = ImageTk.PhotoImage(Image.fromarray(image))
    image_label.config(image=tkimg)

def export_image():
    export_path = filedialog.asksaveasfilename(defaultextension=".png")
    if export_path:
        final_image = Image.fromarray(image)
        final_image.save(export_path)

def set_dpi():
    global DPI, E
    dpi = simpledialog.askinteger("Set DPI", "Enter DPI value:",
                                  initialvalue=DPI, minvalue=1)
    if dpi:
        DPI = dpi
        E = round(2.5*DPI)

def update_slider(value):
    shift = int(value)

    shifted_image = np.roll(original_image, shift, axis=1)

    diff_image = np.abs(original_image.astype(int)
                        -shifted_image.astype(int))
    diff_image = np.clip(diff_image, 0, 255).astype(np.uint8)

    tkimg.paste(Image.fromarray(diff_image)) 
    window.update_idletasks()

def round(x):
    return int(x + 0.5)

def separation(Z):
    return round((1 - mu * Z) * E / (2 - mu * Z))


# Constants
mu = 1 / 3.0

# Global variables
DPI = 100
E = round(2.5 * DPI) # 2.5 Inches
maxsep = separation(0)

# Example Image
texture_img = Image.open(texture_img_path).convert('RGB')
Depthmap = Image.open(Depthmap_path).convert('L')
Z = img_to_arr(Depthmap)
maxX, maxY = Depthmap.width, Depthmap.height
#print("Z(w,h) = " +  str(maxX) + " " +  str(maxY) )
texture_sc = np.array(texture_img) # default

# Drawing functions
def set_pixel(image, x, y, value):
    if 0 <= x < maxX and 0 <= y < maxY:
        image[y, x] = value

def draw_circle(image, xC, yC, radius, color=[0,0,0]):
    for x in range(xC-radius, xC+radius):
        for y in range(yC-radius, yC+radius):
            distance = np.sqrt((x - xC) ** 2 + (y - yC) ** 2)
            if distance <= radius:
                image[y, x] = color

def toggle_circles():
    if switch_var.get():
        c = randrange(237) + 9
        draw_circles([c,c,c])
    else:
        image[:, :, :] = original_image
    tkimg.paste(Image.fromarray(image))
    window.update_idletasks()

def draw_circles(color=[0,0,0]):
    draw_circle(image, maxX // 2 - separation(0) // 2, 
                maxY * 1 // 20, 10, color)
    draw_circle(image, maxX // 2 + separation(0) // 2, 
                maxY * 1 // 20, 10, color)

# Enable/disable buttons during calculations ...
def disable_buttons():
    startbutton.config(state="disabled")
    texture_button.config(state="disabled")
    depth_button.config(state="disabled")
    export_button.config(state="disabled")
    dpi_button.config(state="disabled")
    switch.config(state="disabled")
    slider.config(state="disabled")
    hiddensurface.config(state="disabled")
    R1.config(state="disabled")
    R2.config(state="disabled")
    R3.config(state="disabled")

def enable_buttons():
    startbutton.config(state="normal")
    texture_button.config(state="normal")
    depth_button.config(state="normal")
    export_button.config(state="normal")
    dpi_button.config(state="normal")
    switch.config(state="normal")
    slider.config(state="normal")
    hiddensurface.config(state="normal")
    R1.config(state="normal")
    R2.config(state="normal")
    R3.config(state="normal")


# Tkinter setup
window = tk.Tk()
window.title("STEREOGRAM CREATOR")

s = ttk.Style()
s.configure('TButton', font=('Arial', 10))

# Frame for image and left panel for switches and buttons
right_frame = tk.Frame(window, padx=15, pady=15)
right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

left_frame = tk.Frame(window, padx=15, pady=15)
left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Head image
Head_image_file = Image.open(Head_image_path).resize((352, 228))
Head_image = ImageTk.PhotoImage(Head_image_file)
Head_image_ = tk.Label(left_frame, image=Head_image)
Head_image_.grid(row=1, column=0, padx=0, pady=0, 
                 columnspan=2, sticky=tk.N)

spacer1 = tk.Label(left_frame, text="")
spacer1.grid(row=2, column=0, columnspan=2, pady=20)

# Unputs and buttons
texture_button = ttk.Button(left_frame, text="Import Texture Image", 
                            style='TButton',padding= 5, 
                            command=import_texture_image)
texture_button.grid(row=3, column=0, padx=10, pady=0, sticky=tk.W)

depth_button = ttk.Button(left_frame, text="Import Depth Image", 
                          style='TButton', padding= 5, 
                          command=import_depth_image)
depth_button.grid(row=3, column=1, padx=10, pady=0, sticky=tk.W)

def update_texture_preview():
    texture_img_resized = texture_img.resize((100, 100))
    texture_preview = ImageTk.PhotoImage(texture_img_resized)
    texture_preview_label.config(image=texture_preview)
    texture_preview_label.image = texture_preview

def update_depth_preview():
    depth_image_resized = Depthmap.resize((100, 100))
    depth_preview = ImageTk.PhotoImage(depth_image_resized)
    depth_preview_label.config(image=depth_preview)
    depth_preview_label.image = depth_preview

texture_preview_label = tk.Label(left_frame)
texture_preview_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

depth_preview_label = tk.Label(left_frame)
depth_preview_label.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

dpi_button = ttk.Button(left_frame, text="Set DPI",
                         padding=5, command=set_dpi)
dpi_button.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

hiddensurface_var = tk.BooleanVar(value=True)
hiddensurface = tk.Checkbutton(left_frame, text="Hidden Surface Removal", 
                               variable=hiddensurface_var)
hiddensurface.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

def selR():
    if varR.get() == 1:
        selection = "Selected algorithm: \"Constraint-Left-Right\""
    elif varR.get() == 2:
        selection = "Selected algorithm: \"Constraint-Right-Left\""
    else:
        selection = "Selected algorithm: \"Constraint-Center-Side\""

varR = tk.IntVar(value=1)
varR.set(0)
R1 = tk.Radiobutton(left_frame, text="Left-Right", 
                    variable=varR, value=1, command=selR)
R1.grid(row=6, column=1, padx=10, pady=0, sticky=tk.W)
R2 = tk.Radiobutton(left_frame, text="Right-Left", 
                    variable=varR, value=2, command=selR)
R2.grid(row=7, column=1, padx=10, pady=0, sticky=tk.W)
R3 = tk.Radiobutton(left_frame, text="Center-Side", 
                    variable=varR, value=0, command=selR)
R3.grid(row=8, column=1, padx=10, pady=0, sticky=tk.W)

startbutton = tk.Button(left_frame, text="Create Stereogram", 
                        font=('Arial', 10), background='#444444', 
                        foreground="white", height=2, width=20, 
                        borderwidth=0, highlightthickness=0, 
                        relief='flat', command=lambda: start_drawing())
startbutton.grid(row=9, column=0, padx=10, pady=10, sticky=tk.W)

switch_var = tk.BooleanVar(value=False)
switch = tk.Checkbutton(left_frame, text="Show Circles", variable=switch_var, 
                        command=toggle_circles)
switch.grid(row=10, column=1, padx=10, pady=10, sticky=tk.W)

slider = tk.Scale(left_frame, from_=0, to=200, length=200, showvalue=0, 
                  width=20, font=('Arial', 10), label="Reveal Hidden Image", 
                  orient=tk.HORIZONTAL, command=update_slider)
slider.grid(row=10, column=0, padx=10, pady=10, sticky=tk.W)

export_button = tk.Button(left_frame, text="Export Stereogram", 
                          font=('Arial', 10), bg='#444444', fg="white", 
                          height=2, width=20, borderwidth=0, 
                          highlightthickness=0, relief='flat', 
                          command=export_image)
export_button.grid(row=12, column=0, padx=10, pady=10, sticky=tk.W)


# Configure the main window to be resizable
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
right_frame.columnconfigure(0, weight=1)
right_frame.columnconfigure(1, weight=1)

update_texture_preview()
update_depth_preview()

# Initialize the output image
image = np.ones((maxY, maxX, 3), dtype=np.uint8)*255
tkimg = ImageTk.PhotoImage(Image.fromarray(image))

image_label = tk.Label(right_frame, image=tkimg)
image_label.grid(row=0, column=1, padx=0, pady=0, columnspan=2)

y_global = 0  # Global variable to keep track of the current row
original_image = np.ones((maxY, maxX, 3), dtype=np.uint8)*255
#dbglineNo = 29 # DEBUGGING

# ---------------------------------------------
# Designs based on Thimbleby et al.
# ---------------------------------------------

def draw_autostereogram_LR_line(Z, texture_sc):
    global y_global, original_image

    pix = np.zeros((maxX, 3), dtype=np.uint8)
    constraint = np.arange(maxX)
    y = y_global
    # Iterate over scan line from left to right
    for x in range(maxX):
        s = separation(Z[x, y])
        left = x - s // 2
        right = left + s
        # ---------- DEBUGGING START ------------
        #if y_global==dbglineNo:
        #    mystring = ("x=" + str(x) + " s=" + str(s) + " l=" 
        #                + str(left) + " r=" + str(right) + " ->")
        #whi = 0
        # ---------- DEBUGGING END --------------
 
        if 0 <= left < maxX and 0 <= right < maxX:
            visible = True
            t = 1

            if hiddensurface_var.get() == True: 
                # Hidden surface detection
                m = 2 * (2 - mu * Z[x, y]) / (mu * E)
                zt = Z[x,y]
                while visible:
                    #zt = Z[x, y] + 2 * (2 - mu * Z[x, y]) * t / (mu * E)
                    zt +=m
                    if x - t >= 0 and x + t < maxX:
                        # False if obscured:
                        visible = Z[x - t, y] < zt and Z[x + t, y] < zt
                    t += 1
                    if zt >= 1:
                        break

            if visible == True:
                # Constrain pixel colors
                l = constraint[left]
                while l != left and l != right:
                # left is already constrained and constraint[left] != right
                    if l < right:
                        #whi += 1 # DEBUGGING
                        left = l
                        l = constraint[left]
                    else:
                        #whi += 10 # DEBUGGING
                        constraint[left] = right
                        left = right
                        right = l
                        l = constraint[left]
                constraint[left] = right
                # --------- DEBUGGING START ---------------
                #if y_global==dbglineNo:
                #  x_str = np.array_repr(constraint[50:100]).replace('\n', '')
                #  print(mystring + "whi=" + str(whi) + " -> " + x_str)
                # --------- DEBUGGING END -----------------

    # Assign pixel colours from right to left
    for x in range(maxX - 1, -1, -1):
        if constraint[x] == x:
            pix[x] = texture_sc[y, (x) % maxsep]
        else:
            pix[x] = pix[constraint[x]]
        set_pixel(image, x, y, pix[x])

    tkimg.paste(Image.fromarray(image))
    window.update_idletasks()

    y_global += 1
    if y_global < maxY:
        window.after(1, draw_autostereogram_LR_line, Z, texture_sc)
    else:
        original_image = np.copy(image)
        enable_buttons()

def draw_autostereogram_RL_line(Z, texture_sc):
    global y_global, original_image

    pix = np.zeros((maxX, 3), dtype=np.uint8)
    constraint = np.arange(maxX)
    y = y_global
    # Iterate over scan line from right to left
    for x in range(maxX - 1, -1, -1):
        s = separation(Z[x, y])
        left = x - s // 2
        right = left + s

        if 0 <= left < maxX and 0 <= right < maxX:
            visible = True
            t = 1

            if hiddensurface_var.get() == True: 
                # Hidden surface detection
                m = 2 * (2 - mu * Z[x, y]) / (mu * E)
                zt = Z[x,y]
                while visible:
                    #zt = Z[x, y] + 2 * (2 - mu * Z[x, y]) * t / (mu * E)
                    zt +=m
                    if x - t >= 0 and x + t < maxX:
                        # False if obscured:
                        visible = Z[x - t, y] < zt and Z[x + t, y] < zt
                    t += 1
                    if zt >= 1:
                        break

            if visible == True:
                # Constrain pixel colors
                l = constraint[right]
                while l != left and l != right:
                    if l > left:
                        right = l
                        l = constraint[right]
                    else:
                        constraint[right] = left
                        right = left
                        left = l
                        l = constraint[right] # note right !
                        
                constraint[right] = left 

    # Assign pixel colours from left to right
    for x in range(maxX):
        if constraint[x] == x:
            pix[x] = texture_sc[y, (x) % maxsep]
        else:
            pix[x] = pix[constraint[x]]
        set_pixel(image, x, y, pix[x])

    tkimg.paste(Image.fromarray(image))
    window.update_idletasks()

    y_global += 1
    if y_global < maxY:
        window.after(1, draw_autostereogram_RL_line, Z, texture_sc)
    else:
        original_image = np.copy(image)
        enable_buttons()

# ---------------------------------------------
# Design based on Steer / Techmind.org
# ---------------------------------------------

def draw_autostereogram_NLR_line(Z, texture_sc):
    global y_global, original_image

    pix = np.zeros((maxX, 3), dtype=np.uint8)
    lookL = np.arange(maxX)
    lookR = np.arange(maxX)
    y = y_global
    # Iterate over scan line from left to right
    for x in range(maxX):
        s = separation(Z[x, y])
        left = x - s // 2
        right = left + s
 
        if 0 <= left < maxX and 0 <= right < maxX:
            visible = True

            if hiddensurface_var.get() == True: 
                # Hidden surface detection
                if (lookL[right] != right):   # right pt already linked
                    if (lookL[right] < left): # deeper than current
                        lookR[lookL[right]] = lookL[right] # break old links
                        lookL[right] = right
                    else:
                        visible = False
                if (lookR[left]!=left):       # left pt already linked
                    if (lookR[left] > right): # deeper than current
                        lookL[lookR[left]] = lookR[left]; # break old links
                        lookR[left] = left
                    else: 
                        visible = False

            if visible == True:
                lookL[right] = left
                lookR[left] = right

    # Assign pixel colours from left to right
    lastlinked = -13; # dummy initial value
    for x in range(maxX):
        if lookL[x] == x:
            if lastlinked == (x-1):
                pix[x] = pix[x-1] # probably lone inserted pixel ...
            else:
                #pix[x] = texture_sc[y, (x) % maxsep]
                # use new tex area (y-offset) for fill-in points
                pix[x] = texture_sc[(y + (x//maxsep)*(DPI//16)) % maxY, 
                                    (x) % maxsep]
        else:
            pix[x] = pix[lookL[x]]
            lastlinked = x; # keep track of the last pixel to be constrained

    # Set pixels from left to right
    for x in range(maxX):
        set_pixel(image, x, y, pix[x])

    tkimg.paste(Image.fromarray(image))
    window.update_idletasks()

    y_global += 1
    if y_global < maxY:
        window.after(1, draw_autostereogram_NLR_line, Z, texture_sc)
    else:
        original_image = np.copy(image)
        enable_buttons()

def draw_autostereogram_NCS_line(Z, texture_sc):
    global y_global, original_image

    pix = np.zeros((maxX, 3), dtype=np.uint8)
    lookL = np.arange(maxX)
    lookR = np.arange(maxX)
    y = y_global
    # Iterate over scan line from left to right
    for x in range(maxX):
        s = separation(Z[x, y])
        left = x - s // 2
        right = left + s
 
        if 0 <= left < maxX and 0 <= right < maxX:
            visible = True
            #t = 1

            if hiddensurface_var.get() == True: 
                # Hidden surface detection
                if (lookL[right] != right):   # right pt already linked
                    if (lookL[right] < left): # deeper than current
                        lookR[lookL[right]] = lookL[right] # break old links
                        lookL[right] = right
                    else:
                        visible = False
                if (lookR[left]!=left):       # left pt already linked
                    if (lookR[left] > right): # deeper than current
                        lookL[lookR[left]] = lookR[left]; # break old links
                        lookR[left] = left
                    else: 
                        visible = False

            if visible == True:
                lookL[right] = left
                lookR[left] = right

    # Assign pixel colours from "center-maxsep/2" (s) to right
    s = maxX//2 - maxsep//2; 
    poffset = maxsep - (s % maxsep)
    lastlinked = -13; # dummy initial value
    for x in range(s, maxX, 1):
        if (lookL[x] == x) or (lookL[x] < s): # ignore constraints beyond s
            if lastlinked == (x-1):
                pix[x] = pix[x-1] # probably lone inserted pixel ...
            else:
                #pix[x] = texture_sc[y, (x+poffset) % maxsep]
                # use new tex area (y-offset) 4 fill-in points beyond ...
                pix[x] = texture_sc[(y + ((x-s)//maxsep)*(DPI//16)) % maxY, 
                                    (x+poffset) % maxsep]
        else:
            pix[x] = pix[lookL[x]]
            lastlinked = x; # keep track of the last pixel to be constrained

    # Assign pixel colours from "center-maxsep/2-1" (s-1) to left
    lastlinked = -13; # dummy initial value
    for x in range(s-1, -1, -1):
        if lookR[x] == x:
            if lastlinked == (x+1):
                pix[x] = pix[x+1] # probably lone inserted pixel ...
            else:
                #pix[x] = texture_sc[y, (x+poffset) % maxsep]
                # use new tex area (y-offset) 4 fill-in points beyond ...
                pix[x] = texture_sc[(y + ((s-x)//(maxsep+1))*(DPI//16)) % maxY, 
                                    (x+poffset) % maxsep]
        else:
            pix[x] = pix[lookR[x]]
            lastlinked = x; # keep track of the last pixel to be constrained

    # Set pixels from left to right
    for x in range(maxX):
        set_pixel(image, x, y, pix[x])

    y_global += 1

    tkimg.paste(Image.fromarray(image))
    window.update_idletasks()

#   N = 2
#   if y_global % N == 0 or y_global >= maxY:
#       tkimg.paste(Image.fromarray(image))
#       window.update_idletasks()

    if y_global < maxY:
        window.after(1, draw_autostereogram_NCS_line, Z, texture_sc)
    else:
        original_image = np.copy(image)
        enable_buttons()

# ---------------------------------------------

def start_drawing():
    global y_global, texture_sc
    y_global = 0
    disable_buttons()
    #print("maxsep = " + str(maxsep))
    if (texture_img.width < maxsep) and (texture_img.height < maxY):
        texture_sc = np.array(texture_img.resize((maxsep, maxY)))
    elif (texture_img.width < maxsep):
        texture_sc = np.array(texture_img.resize((maxsep,
                                                 texture_img.height)))
    elif (texture_img.height < maxY):
        texture_sc = np.array(texture_img.resize((texture_img.width, maxY)))
    else:
        texture_sc = np.array(texture_img)
    #selection = "executing algorithm " + str(varR.get())
    #print(selection)
    if varR.get() == 1:
        window.after(0, draw_autostereogram_LR_line, Z, texture_sc)
    elif varR.get() == 2:
        window.after(0, draw_autostereogram_RL_line, Z, texture_sc)
    elif varR.get() == 0:
        #window.after(0, draw_autostereogram_NLR_line, Z, texture_sc)
        window.after(0, draw_autostereogram_NCS_line, Z, texture_sc)

window.mainloop()
