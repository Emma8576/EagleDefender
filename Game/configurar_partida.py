import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame 

#hacer variables de fuentes globales
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
fuente_retro_6 = ("8-Bit Operator+ 8", 70)
fuente_retro_7 = ("8-Bit Operator+ 8", 60)
fuente_retro_8 = ("8-Bit Operator+ 8", 35)
fuente_retro_9 = ("8-Bit Operator+ 8", 12)

#Se agrega imagen de fondo
def cargar_imagen_de_fondo(ventana_1, ruta_imagen):
    # Cargar la imagen de fondo
    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)
    return imagen


#Función ventana configurar partida
def configurar_partida():
    global ventana_1, seleccion
    ventana_1= tk.Tk()
    ventana_1.attributes("-fullscreen", True)
    
    # Establecer el título de la ventana
    ventana_1.title("Bienvenidos")

    # Cargar icono de la ventana
    ventana_1.iconbitmap("loginImages/icon.ico")

    # Obtener la imagen de fondo
    fondo_imagen = cargar_imagen_de_fondo(ventana_1, "loginImages/fondo1.png")
    
    # Crear un Label para mostrar la imagen de fondo
    fondo_label = Label(ventana_1, image=fondo_imagen)
    fondo_label.place(relx=0.5, rely=0.5, anchor='center')
    
    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana_1, text="Battle City", bg="#000030", font=fuente_retro_6, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5, anchor='center') 
    etiqueta_retro.pack()
    
    # Función para mostrar el menú 1 en la posición del botón
    def mostrar_menu(event):
        menu_principal.post(event.x_root, event.y_root)

    # Función para mostrar el menú 1 en la posición del botón
    def mostrar_menu_2(event):
        menu_principal_2.post(event.x_root, event.y_root)
        
    # Crear un botón que actúa como un menú desplegable
    boton_menu = tk.Button(ventana_1, text="Elegir música de Victoria", font=fuente_retro_5, bg="blue", fg="white", activebackground="#101654")
    boton_menu.place(relx=0.5 - 0.38, rely=0.5 - 0.20)

    # Crear un menú desplegable
    menu_principal = Menu(ventana_1, tearoff=0)
    menu_principal.add_command(label="Insertar canción 1", font= fuente_retro_9, foreground= "white", background="#101654", command=lambda: print("Cancion 1"))
    menu_principal.add_command(label="Insertar canción 2", font= fuente_retro_9, foreground= "white",  background="#101654", command=lambda: print("Cancion 2"))
    menu_principal.add_command(label="Insertar canción 3", font= fuente_retro_9, foreground= "white",  background="#101654", command=lambda: print("Cancion 3"))
    menu_principal.add_command(label="Insertar canción 4", font= fuente_retro_9, foreground= "white",  background="#101654", command=lambda: print("Cancion 4"))
    menu_principal.add_command(label="Insertar canción 5", font= fuente_retro_9, foreground= "white",  background="#101654", command=lambda: print("Cancion 5"))

    # Asociar la función mostrar_menu al evento de clic en el botón
    boton_menu.bind("<Button-1>", mostrar_menu)
    
    
    # Crear el segundo botón y menú desplegable
    boton_menu_2 = tk.Button(ventana_1, text="Elegir música de Victoria", font=fuente_retro_5, bg="blue", fg="white", activebackground="#101654")
    boton_menu_2.place(relx=0.5 + 0.15, rely=0.5 - 0.20)

    menu_principal_2 = Menu(ventana_1, tearoff=0)
    menu_principal_2.add_command(label="Insertar canción 1", font= fuente_retro_9, foreground= "white", background="#101654", command=lambda: print("Cancion 1"))
    menu_principal_2.add_command(label="Insertar canción 2", font= fuente_retro_9, foreground= "white", background="#101654", command=lambda: print("Cancion 2"))

    boton_menu_2.bind("<Button-1>", mostrar_menu_2)

    #Etiqueta de Configurar partida
    ancho_pantalla = ventana_1.winfo_screenwidth()
    global etiqueta
    etiqueta = Label(ventana_1, text="Configurar partida", bg="#101654", fg="white", font=fuente_retro_8)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=100) 

    #Etiqueta de jugador 1
    ancho_pantalla_1 = ventana_1.winfo_screenwidth()
    global etiqueta_jugador_1
    etiqueta_jugador_1 = Label(ventana_1, text="Defensor", bg="#101654", fg="white", font=fuente_retro_8)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla_1 - etiqueta.winfo_reqwidth()) // 4
    etiqueta_jugador_1.place(x=x, y=150) 


    #Etiqueta de jugador 2
    ancho_pantalla_2 = ventana_1.winfo_screenwidth()
    global etiqueta_jugador_2
    etiqueta_jugador_2 = Label(ventana_1, text="Atacante", bg="#101654", fg="white", font=fuente_retro_8)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla_2 - etiqueta.winfo_reqwidth()) * 1.1
    etiqueta_jugador_2.place(x=x, y=150) 

    # Botón de Iniciar Partida
    global boton_inicio
    boton_inicio = tk.Button(ventana_1,cursor="exchange", text="Iniciar partida", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_5, relief="raised", borderwidth=10, command="")
    boton_inicio.place(relx=0.5+ 0.25, rely=0.5 + 0.35, anchor='center')

    # Espacio entre botones
    espacio_entre_botones = 30 
    
    # Botón de Salir
    global boton_salir
    boton_salir = tk.Button(ventana_1,cursor="exchange", text="Regresar", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_5, relief="raised", borderwidth=10, command=ventana_1.destroy)
    boton_salir.place(relx=0.5 - 0.25, rely=0.5 + 0.35, anchor='center')


    global boton_configuración 
    boton_configuración = tk.Button(ventana_1,cursor="exchange", text="Configuración", background = "#0a0c3f", fg="white", font=("System 18 bold"), relief="raised", command="")
    boton_configuración.pack()
    boton_configuración.place(x=0, y=0, height=40, width=200)

    # Mostrar la ventana principal
    ventana_1.mainloop()
    
configurar_partida()



