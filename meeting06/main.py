from tkinter import *
from tkinter import ttk
from random import randint

press=True
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Random Roll!").grid(column=0, row=0)
# result_label = ttk.Label(frm, text="-", font=("Arial", 16))
# result_label.grid(column=2, row=0, padx=5)
# a=2

# a = randint(1, 6)

# roll_dice()    


photo1 = PhotoImage(file="resources/1.png")
photo2 = PhotoImage(file="resources/2.png")
photo3 = PhotoImage(file="resources/3.png")
photo4 = PhotoImage(file="resources/4.png")
photo5 = PhotoImage(file="resources/5.png")
photo6 = PhotoImage(file="resources/6.png")
# image_label = Label(root, image=photo1)
# image_label = Label(frm, image=photo1)
# photoa=eval(f"photo{a}")
a = randint(1, 6)
photoa = eval(f"photo{a}")
image_label = Label(frm, image=photoa)
image_label.grid(column=2, row=0, padx=5)
def roll_dice():
    global a, photoa
    a = randint(1, 6)
    photoa = eval(f"photo{a}")
    match(a):
        case 1:
            image_label.config(image=photo1)
        case 2:
            image_label.config(image=photo2)

        case 3:
            image_label.config(image=photo3)
        case 4:
            image_label.config(image=photo4)
        case 5:
            image_label.config(image=photo5)
        case 6:
            image_label.config(image=photo6)

image_label = Label(frm, image=photoa)
image_label.grid(column=2, row=0, padx=5)
ttk.Button(frm, text="Roll", command=roll_dice).grid(column=2, row=1, padx=5)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=2, padx=5)

root.mainloop()