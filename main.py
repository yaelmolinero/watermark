from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image as PImage, ImageDraw, ImageFont
from time import sleep
import os

TEXT_FONT = ('Arial', 14, 'normal')
BTN_FONT = ('Arial', 12, 'bold')
COLOR_WIDGETS = '#4C0AB9'
ACTIVE_COLOR_W = '#56144C'
COLOR_TEXT = '#fff'
IMAGE_PATH = ""
color_text_rgb = (255, 255, 255)
is_saved = False


def open_file():
    global IMAGE_PATH, is_saved, show_image, my_canvas, img, txt, draw_img

    is_saved = False
    IMAGE_PATH = ""
    IMAGE_PATH = askopenfilename(defaultextension=None, filetypes=[('jpeg', '.jpg .jpeg'),
                                                                   ('png', '.png')])
    if IMAGE_PATH == "":
        return
    img = PImage.open(IMAGE_PATH).convert('RGBA')
    open_btn.destroy()
    sleep(0.5)

    if img.width > 750 or img.height > 600:
        for n in range(4):
            new_width = int(img.width / 2)
            new_height = int(img.height / 2)
            img = img.resize((new_width, new_height), PImage.LANCZOS)
            if img.width < 750 and img.height < 600:
                break

    txt = PImage.new('RGBA', img.size, (255, 255, 255, 0))
    draw_img = ImageDraw.Draw(txt)

    my_canvas = Canvas(image_frm, width=img.width, height=img.height, highlightthickness=0, bg='#202020')
    my_canvas.pack(expand=True)
    my_canvas.bind('<B1-Motion>', move)

    show_image = ImageTk.PhotoImage(img)
    my_canvas.create_image(img.width / 2, img.height / 2, image=show_image)
    my_canvas.update()

    new_btn.state(['!disabled'])


def new_text():
    global my_mark

    marker_input.state(['!disabled'])
    marker_input.focus()
    marker_input.select_present()
    try:
        add_text()
    except NameError:
        pass
    my_mark = my_canvas.create_text(img.width / 2, img.height / 2, text="",
                                    fill=COLOR_TEXT, font=(mark_font, mark_size, mark_weight))


def add_text():
    coo = my_canvas.coords(my_mark)
    color_text_rgba = list(color_text_rgb)
    color_text_rgba.append(int(opacity.get()))
    fnt = ImageFont.truetype('ariblk.ttf', mark_size)

    draw_img.text((coo[0], coo[1]), marker_input.get(), tuple(color_text_rgba), fnt, anchor='mm')


def writing(*args):
    value = marker_input.get()
    my_canvas.itemconfig(my_mark, text=value)


def pick_color():
    global COLOR_TEXT, color_text_rgb

    color = askcolor(title='Chose a Color')
    color_text_rgb = color[0]
    COLOR_TEXT = color[1]
    s.configure('color.TButton', background=COLOR_TEXT, foreground=COLOR_TEXT)
    s.map('color.TButton', background=[('active', COLOR_TEXT)])
    try:
        my_canvas.itemconfig(my_mark, fill=COLOR_TEXT)
    except NameError:
        pass


def change(*args):
    global mark_size

    value = text_size.get()
    if value == "":
        mark_size = 1
    else:
        mark_size = int(value)
    try:
        my_canvas.itemconfig(my_mark, font=(mark_font, mark_size, mark_weight))
    except NameError:
        pass


def move(event):
    x, y = event.x, event.y
    my_canvas.coords(my_mark, x, y)


def save():
    if IMAGE_PATH == "":
        return
    try:
        add_text()
    except NameError:
        pass
    out = PImage.alpha_composite(img, txt)
    file_path = asksaveasfilename(confirmoverwrite=True,
                                  defaultextension='png',
                                  filetypes=[('jpeg', '.jpeg .jpg'),
                                             ('png', '.png')])
    if file_path is not None:
        if os.path.splitext(file_path)[1] in ['.jpeg', '.jpg']:
            out = out.convert('RGB')
        out.save(fp=file_path)
        out.show(title=file_path.split('/')[-1])
        global is_saved
        is_saved = True

def close():
    if is_saved:
        if askyesno(message='Do you want to continue?', title='Close'):
            window.destroy()
    else:
        window.destroy()

def close_img():
    global open_btn

    try:
        my_canvas.destroy()
        open_btn = ttk.Button(image_frm, text='Open a file.', width=25, padding=100, style='btn_img.TButton',
                              command=open_file)
        open_btn.pack(expand=True)
    except NameError:
        pass

def reset():
    try:
        my_canvas.destroy()
    except NameError:
        pass
    open_file()


# --------------- WINDOW SETTING --------------- #
window = Tk()
window.title("Watermark App")
window.geometry("1100x600")  # Initial size of the window
window.resizable(False, False)  # Size can't be change

# --------------- STYLE --------------- #
s = ttk.Style()
s.theme_use('alt')
s.configure('TButton', background='#343434', foreground='white', borderwidth=0, font=BTN_FONT, relief='flat')
s.map('TButton', background=[('active', '#3E3E3E')])

s.configure('TLabel', background='#2C2C2C', foreground='white', justify='left', font=TEXT_FONT)

s.configure('TEntry', fieldbackground='#202020', background='#202020', foreground='white')
s.configure('TSpinbox', fieldbackground='#202020', foreground='white')

s.configure('TScale', background='#2C2C2C')
s.map('TScale', background=[('active', COLOR_WIDGETS)])

s.configure('TSeparator', foreground='white')
# s.configure('TSpinbox', background='#000')

########## IMAGE frame ##########
s.configure('img_frame.TFrame', background='#202020')
# Button load image
s.configure('btn_img.TButton', background='#2A2A2A', relief='flat')
s.map('btn_img.TButton', background=[('active', '#343434')])

########## TOOLS frame ##########
s.configure('tool_frame.TFrame', background='#2C2C2C')
# Button
s.configure('tool_btn.TButton', background=COLOR_WIDGETS)
s.map('tool_btn.TButton', background=[('active', ACTIVE_COLOR_W)])
s.configure('color.TButton', background=COLOR_TEXT, foreground=COLOR_TEXT)
s.map('color.TButton', background=[('active', COLOR_TEXT)])
# Label
s.configure('title_frm.TLabel', font=('Arial', 14, 'bold'), justify=CENTER)

# --------------- SHOW IMAGE --------------- #
image_frm = ttk.Frame(window, width=750, height=600, style='img_frame.TFrame')
image_frm.pack_propagate(False)  # No auto shrink or grow
image_frm.pack(fill=BOTH, side=LEFT)

menu_bar = Menu(bg='#2C2C2C', fg='white')
menu_options = Menu(menu_bar, tearoff=False, bg='#202020', fg='white', borderwidth=0)
menu_options.add_command(label="Open file", accelerator="Ctrl+O", command=reset)
menu_options.add_command(label="Close file", accelerator="Ctrl+C", command=close_img)

menu_bar.add_cascade(menu=menu_options, label='File')
window.configure(menu=menu_bar)

open_btn = ttk.Button(image_frm, text='Open a file.', width=25, padding=100, style='btn_img.TButton',
                      command=open_file)
open_btn.pack(expand=True)

# --------------- SHOW TOOLS --------------- #
tool_frm = ttk.Frame(window, width=350, height=600, padding=25, style='tool_frame.TFrame')
tool_frm.pack_propagate(False)  # No auto shrink or grow
tool_frm.grid_propagate(False)
tool_frm.pack(fill=BOTH, side=RIGHT)

ttk.Label(tool_frm, text='Watermark Text', style='title_frm.TLabel') \
    .grid(row=0, column=0, columnspan=2, sticky='we')
ttk.Separator(tool_frm).grid(row=1, column=0, columnspan=2, pady=15, sticky='we')

text_input = StringVar(value="Enter your mark here.")
marker_input = ttk.Entry(tool_frm, width=32, textvariable=text_input, font=('Arial', 12, 'bold'), state='disabled')
marker_input.grid(row=2, column=0, columnspan=2, sticky='w', pady=15)
text_input.trace_add('write', writing)
new_btn = ttk.Button(tool_frm, text='+ New', padding=5, command=new_text, state='disabled')
new_btn.grid(row=3, column=0, columnspan=2, sticky='we')

ttk.Label(tool_frm, text='Text size: ').grid(row=4, column=0, pady=15, sticky='we')
number_input = IntVar(value=14)
text_size = ttk.Spinbox(tool_frm, width=5, from_=1, to=95, increment=1, textvariable=number_input)
text_size.grid(row=4, column=1, pady=15, sticky='e')
number_input.trace_add('write', change)

ttk.Label(tool_frm, text='Opacity: ').grid(row=5, column=0, pady=15, sticky='we')
opacity = ttk.Scale(tool_frm, from_=0, to=255, variable=IntVar(value=125))
opacity.grid(row=5, column=1, pady=15, sticky='we')

ttk.Label(tool_frm, text='Color: ').grid(row=6, column=0, pady=15, sticky='we')
ttk.Button(tool_frm, text='COLOR', padding=5, style='color.TButton', command=pick_color) \
    .grid(row=6, column=1, pady=15, sticky='we')

ttk.Label(tool_frm, text="Invisible Label", background='#2C2C2C', foreground='#2C2C2C') \
    .grid(row=7, columnspan=2, pady=70, sticky='we')

ttk.Button(tool_frm, text='Confirm', padding=5, style='tool_btn.TButton', command=save) \
    .grid(row=8, column=0, padx=5, pady=15, sticky='we')
ttk.Button(tool_frm, text='Cancel', padding=5, command=close) \
    .grid(row=8, column=1, padx=5, pady=15, sticky='we')

mark_font, mark_size, mark_weight = 'Arial', int(text_size.get()), 'bold'
window.mainloop()
