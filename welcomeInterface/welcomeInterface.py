import tkinter as tk
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.title("Reproducción de GIF en bucle")

# Cargar el GIF
gif_path = "welcomeInterfaceFramesSprites/mainWelcome2/mainWelcome1 (1).gif"
gif = Image.open(gif_path)
frame_count = gif.n_frames
frames = [ImageTk.PhotoImage(gif.copy().seek(i)) for i in range(frame_count)]

# Mostrar el GIF en un Label
label = tk.Label(root)
label.pack()

# Función para actualizar el GIF
def update_frame(idx):
    frame = frames[idx]
    label.configure(image=frame)
    root.after(100, update_frame, (idx + 1) % frame_count)

# Iniciar la actualización del GIF
update_frame(0)

# Iniciar la aplicación
root.mainloop()
