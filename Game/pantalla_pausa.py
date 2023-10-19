import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Crear la ventana principal de tkinter y ocultarla
root = tk.Tk()
root.withdraw()

# Definir variables globales con el formato palabra_otra_palabra
global fuente_retro
global fuente_retro_1
global fuente_retro_2
global fuente_retro_3
global fuente_retro_4
global fuente_retro_5

# Se añade la fuente retro en diversos tamaños
fuente_retro = ("8-Bit Operator+ 8", 100)
fuente_retro_1 = ("8-Bit Operator+ 8", 40)
fuente_retro_2 = ("8-Bit Operator+ 8", 50)
fuente_retro_3 = ("8-Bit Operator+ 8", 25)
fuente_retro_4 = ("8-Bit Operator+ 8", 20)
fuente_retro_5 = ("8-Bit Operator+ 8", 15)

#abrir ventana de configurción
def abrir_ventana_configuracion(ventana_configuracion):
    # Crea una instancia de la ventana de configuración como una ventana secundaria
    ventana_configuracion = Toplevel(root)
    # Muestra la ventana de configuración
    abrir_configuracion(ventana_configuracion)
    
# Se agrega imagen de fondo
def cargar_imagen_de_fondo(ventana, ruta_imagen):
    # Cargar la imagen de fondo
    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)

    # Crear una etiqueta para mostrar la imagen de fondo
    etiqueta_fondo = Label(ventana, image=imagen)
    etiqueta_fondo.image = imagen  # Mantener una referencia a la imagen
    etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Cubrir toda la ventana

# Función ventana_pausa
def ventana_pausa():
    # Crear una instancia de la ventana de pausa
    ventana_pausa = Toplevel(root)

    # Cargar imagen de fondo en la ventana de pausa
    cargar_imagen_de_fondo(ventana_pausa, "loginImages/fondo1.png")
    ventana_pausa.attributes("-fullscreen", True)
    # Establecer el título de la ventana
    ventana_pausa.title("Pausa en el juego")

    # Cargar icono de la ventana
    ventana_pausa.iconbitmap("loginImages/icon.ico")

    # Etiqueta con el título de la pausa
    etiqueta_titulo_pausa = Label(ventana_pausa, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_titulo_pausa.place(relx=0.5, rely=0.5, anchor='center')
    etiqueta_titulo_pausa.pack()

    # Etiqueta de opciones en la pausa
    ancho_pantalla = ventana_pausa.winfo_screenwidth()
    global etiqueta_pausa
    etiqueta_pausa = Label(ventana_pausa, text="Juego pausado", bg="#101654", fg="white", font=fuente_retro_2)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta_pausa.winfo_reqwidth()) // 2
    etiqueta_pausa.place(x=x, y=200)

    # Botón para reanudar el juego
    boton_reanudar = tk.Button(ventana_pausa, cursor="exchange", text="Reanudar juego", height="5", width="30", background="#0a0c3f", fg="white", font=fuente_retro_5, relief="raised", borderwidth=10, command="")
    boton_reanudar.place(relx=0.5 + 0.25, rely=0.5 + 0.25, anchor='center')

    # Espacio entre botones
    espacio_entre_botones = 30

    # Botón para salir del juego
    boton_salir_juego = tk.Button(ventana_pausa, cursor="exchange", text="Salir del juego", height="5", width="30", background="#0a0c3f", fg="white", font=fuente_retro_5, relief="raised", borderwidth=10, command=root.destroy)
    boton_salir_juego.place(relx=0.5 - 0.25, rely=0.5 + 0.25, anchor='center')

    # Botón para configuración
    boton_configuracion_pausa = tk.Button(ventana_pausa, cursor="exchange", text="Configuración", background="#0a0c3f", fg="white", font=("System 18 bold"), relief="raised", command=lambda: abrir_ventana_configuracion(ventana_pausa))
    boton_configuracion_pausa.pack()
    boton_configuracion_pausa.place(relx=0.5 + 0.35, rely=0, height=40, width=200)

    # Botón para cómo jugar
    boton_como_jugar_pausa = tk.Button(ventana_pausa, cursor="exchange", text="Cómo Jugar", background="#0a0c3f", fg="white", font=("System 18 bold"), relief="raised", command="")
    boton_como_jugar_pausa.pack()
    boton_como_jugar_pausa.place(relx=0.006, rely=0, height=40, width=200)

    # Mostrar la ventana de pausa
    ventana_pausa.mainloop()
    
ventana_pausa()