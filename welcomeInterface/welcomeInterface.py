import tkinter as tk
from PIL import Image

window = tk.Tk()

file1 = 'C:/Users/User/Documents/EagleDefender/welcomeInterface/welcomeInterfaceFramesSprites/SavedItems/mainWelcome2.gif'

info = Image.open(file1)
frames = info.n_frames
imageObject = [PhotoImage(file = file1, format = f"gif - index {1}") for i in range(frames)]
count = 0
showAnimation = None
def animiation(count):
    global showAnimation
    newImage = imageObject[count]

gif_Label = Label(root, image="")
gif_label.place(x=0, y= 0, width= 1245, height= 700)

animation(count)


window.mainloop()