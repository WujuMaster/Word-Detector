from PIL import ImageTk, ImageOps
import PIL.Image
from tkinter import *
from tkinter import filedialog
from utils import detectWords

def openfn():
    filename = filedialog.askopenfilename(title='open')
    return filename
    
def open_img():
    x = openfn()
    img = PIL.Image.open(x)
    img = ImageOps.grayscale(img)
    w, h = img.size
    img = PIL.Image.fromarray(detectWords(img))
    img = img.resize((500, round(500*h/w)), PIL.Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img
    panel.place(relx=0.75, rely=0.5, anchor=CENTER)

root = Tk()
root.title("Words Detector")
root.geometry("1200x800+300+200")
root.resizable(width=True, height=True)

lbl = Label(root, text="Words Detector", font=("Arial Bold", 40))
lbl.place(relx=0.25, rely=0.3, anchor=CENTER)

lbl = Label(root, text="Select an image to detect words", font=("Arial", 20))
lbl.place(relx=0.25, rely=0.4, anchor=CENTER)

panel = Label(root, image=None)

btn = Button(root, text='Browse image', font=("Arial", 10), height=5, width=20, command=open_img)
btn.place(relx=0.25, rely=0.6, anchor=CENTER)

root.mainloop()