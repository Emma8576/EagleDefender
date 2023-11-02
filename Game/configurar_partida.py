import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pygame
from PIL import Image, ImageTk
import subprocess
import sys
import time

pygame.init() 

# hacer variables de fuentes globales
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



# Se agrega imagen de fondo
def cargar_imagen_de_fondo(ventana_1, ruta_imagen):
    # Cargar la imagen de fondo
    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)
    return imagen


def volver_inicio_sesion():
    archivo = 'Game/Login.py'
    try:
        subprocess.Popen(['python', archivo])
        time.sleep(1.5)
        sys.exit()
    except FileNotFoundError:
        print(f'El archivo "{archivo}" no se encontró o no se pudo ejecutar.')


# Función para cargar los nombres de usuario que iniciaron sesión
def cargar_nombres_usuarios():
    with open('nombres_usuarios.txt', 'r') as file:
        lineas = file.readlines()
        usuario_1 = lineas[0].strip().split(": ")[1]
        usuario_2 = lineas[1].strip().split(": ")[1]
        return usuario_1, usuario_2


# Funciones para actualizar las etiquetas de roles
def seleccionar_defensor(usuario):
    etiqueta_jugador_1.config(text=f"Defensor: {usuario}")


def seleccionar_atacante(usuario):
    etiqueta_jugador_2.config(text=f"Atacante: {usuario}")

# Función del botón de iniciar la partida
def iniciar_partida():
    archivo_partida = 'Game/panel.py'
    # obtener los nombres de usuario y roles seleccionados
    usuario_defensor = etiqueta_jugador_1.cget("text").split(": ")[1]
    usuario_atacante = etiqueta_jugador_2.cget("text").split(": ")[1]
    
    # Guardar los roles en el archivo de texto
    with open('Game/nombres_usuarios.txt', 'w') as file:
        file.write(f"Defensor: {usuario_defensor}\n")
        file.write(f"Atacante: {usuario_atacante}\n")
        
    try:
        subprocess.Popen(['python', archivo_partida])
        time.sleep(1)
        sys.exit()
    except FileNotFoundError:
        print(f'El archivo "{archivo_partida}" no se encontró o no se pudo ejecutar.')
        
# Función ventana configurar partida
def configurar_partida():
    global is_playing  # Declarar is_playing como una variable global
    is_playing = False  # Inicializarla con un valor
    global ventana_1, seleccion
    ventana_1 = tk.Tk()
    ventana_1.attributes("-fullscreen", True)

    # Cargar los nombres de usuario
    usuario_1, usuario_2 = cargar_nombres_usuarios()

    # Establecer el título de la ventana
    ventana_1.title("Bienvenidos")

    # Cargar icono de la ventana
    ventana_1.iconbitmap("loginImages/icon.ico")

    # Obtener la imagen de fondo
    fondo_imagen = cargar_imagen_de_fondo(ventana_1, "loginImages/fondo1.png")

    # Crear un Label para mostrar la imagen de fondo
    fondo_label = Label(ventana_1, image=fondo_imagen)
    fondo_label.place(relx=0.5, rely=0.5, anchor='center')

    # Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana_1, text="Battle City", bg="#000030", font=fuente_retro_6, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5, anchor='center')
    etiqueta_retro.pack()

    # Función para mostrar el menú del defensor en la posición del botón
    def mostrar_menu(event):
        menu_principal.post(event.x_root, event.y_root)
        sys.stdout.flush()

    # Función para mostrar el menú del atacante en la posición del botón
    def mostrar_menu_2(event):
        menu_principal_2.post(event.x_root, event.y_root)
        sys.stdout.flush()

    # Función para mostrar el menú de los roles en la posición del botón
    def mostrar_menu_3(event):
        menu_principal_3.delete(0, "end")
        usuarios = cargar_nombres_usuarios()
        for usuario in usuarios:
            menu_principal_3.add_command(label=usuario, font=fuente_retro_9, foreground="white", background="#101654",
                                         command=lambda u=usuario: seleccionar_defensor(u))
        menu_principal_3.post(event.x_root, event.y_root)

    def seleccionar_defensor(usuario):
        etiqueta_jugador_1.config(text=f"Defensor: {usuario}")
        otros_usuarios = [u for u in cargar_nombres_usuarios() if u != usuario]
        if otros_usuarios:
            seleccionar_atacante(otros_usuarios[0])
        # Imprimir el usuario en la terminal
        print(f"El usuario defensor es: {usuario}")

    # Crear un botón que actúa como un menú desplegable del defensor
    boton_menu = tk.Button(ventana_1, text="Elegir música de Victoria", font=fuente_retro_5, bg="#101654", fg="white",
                           activebackground="blue", relief="groove", border=5)
    boton_menu.place(relx=0.5 - 0.38, rely=0.7 - 0.20)

#######

    # Add a list to store selected songs
    selected_songs = [None, None, None, None, None]

    # Create radio buttons to mark favorite songs
    favorite_song = tk.IntVar()
    
#######seleccionar canciones

    # Crear un Listbox para mostrar las canciones seleccionadas
    lista_canciones = tk.Listbox(ventana_1, selectmode=tk.SINGLE, width=30, height=6, font=fuente_retro_9, foreground="black",
                               background="SkyBlue3")
    lista_canciones.place(x=200, y=450)  # Ajusta la posición según tu diseño

    def actualizar_lista_canciones():
        # Borrar cualquier elemento existente en el Listbox
        lista_canciones.delete(0, tk.END)

        # Agregar las canciones seleccionadas al Listbox
        for cancion in canciones_seleccionadas:
            lista_canciones.insert(tk.END, cancion)

    # Luego de que se seleccionen canciones en la función `añadir`, llama a la función `actualizar_lista_canciones`
    # para mostrar las canciones en el Listbox
    def añadir():
        canciones = filedialog.askopenfilenames(initialdir="/", title="Adjunte las canciones", filetypes=(("Archivos MP3", "*.mp3"), ("Todos los archivos", "*.*")))

        # Agregar las rutas de las canciones seleccionadas a la lista
        for cancion in canciones:
            nombre_cancion = cancion.split("/")[-1]  # Opcional: eliminar parte de la ruta
            canciones_seleccionadas.append(nombre_cancion)

        # Actualizar la lista de canciones en el Listbox
        actualizar_lista_canciones()
 
    # Crear una lista para almacenar las rutas de las canciones
    canciones_seleccionadas = []

    # Crear un menú desplegable
    menu_principal = Menu(ventana_1, tearoff=0)
    menu_principal.add_command(label="Insertar canciones", font=fuente_retro_9, foreground="white",
                               background="#101654", command=añadir)
    
    
   

    # Asociar la función mostrar_menu al evento de clic en el botón
    boton_menu.bind("<Button-1>", mostrar_menu)

    # Crear el botón y menú desplegable del atacante
    boton_menu_2 = tk.Button(ventana_1, text="Elegir música de Victoria", font=fuente_retro_5, bg="#101654", fg="white",
                             activebackground="blue", relief="groove", border=5)
    boton_menu_2.place(relx=0.5 + 0.15, rely=0.7 - 0.20)

    menu_principal_2 = Menu(ventana_1, tearoff=0)
    menu_principal_2.add_command(label="Insertar canción 1", font=fuente_retro_9, foreground="white",
                                 background="#101654", command=lambda: print("Cancion 1"))
    menu_principal_2.add_command(label="Insertar canción 2", font=fuente_retro_9, foreground="white",
                                 background="#101654", command=lambda: print("Cancion 2"))

    boton_menu_2.bind("<Button-1>", mostrar_menu_2)

    # Crear el botón y menú desplegable de los roles
    boton_menu_3 = tk.Button(ventana_1, text="Usuarios ⬇", font=fuente_retro_5, bg="#101654", fg="white",
                             activebackground="blue", width=20, height=3, relief="groove", border=5)
    boton_menu_3.place(relx=0.5 - 0.09, rely=0.3 - 0.05)

    menu_principal_3 = Menu(ventana_1, tearoff=0)

    boton_menu_3.bind("<Button-1>", mostrar_menu_3)

    # Etiqueta de Configurar partida
    ancho_pantalla = ventana_1.winfo_screenwidth()
    global etiqueta
    etiqueta = Label(ventana_1, text="Configurar partida", bg="#101654", fg="white", font=fuente_retro_8)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=100)

    # Etiqueta de jugador 1
    ancho_pantalla_1 = ventana_1.winfo_screenwidth()
    global etiqueta_jugador_1
    etiqueta_jugador_1 = Label(ventana_1, text="Defensor: ¿?", bg="#101654", fg="white",
                               font=fuente_retro_3, height=2, width=20)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla_1 - etiqueta.winfo_reqwidth()) // 7
    etiqueta_jugador_1.place(x=x, y=300)

    # Etiqueta de jugador 2
    ancho_pantalla_2 = ventana_1.winfo_screenwidth()
    global etiqueta_jugador_2
    etiqueta_jugador_2 = Label(ventana_1, text="Atacante: ¿?", bg="#101654", fg="white",
                               font=fuente_retro_3, height=2, width=20)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla_2 - etiqueta.winfo_reqwidth()) * 1
    etiqueta_jugador_2.place(x=x, y=300)

    # Etiqueta de jugador rol
    ancho_pantalla_1 = ventana_1.winfo_screenwidth()
    global etiqueta_roless
    etiqueta_roles = Label(ventana_1, text="Elige el usuario defensor", bg="#101654", fg="white",
                           font=fuente_retro_4)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla_1 - etiqueta.winfo_reqwidth()) // 4
    etiqueta_roles.place(relx=0.5 - 0.15, rely=0.5 - 0.3)

    # Botón de Iniciar Partida
    global boton_inicio
    boton_inicio = tk.Button(ventana_1, cursor="exchange", text="Iniciar partida", height="4", width="30",
                             background="#0a0c3f", fg="white", font=fuente_retro_5, relief="raised",
                             borderwidth=10, command=iniciar_partida)
    boton_inicio.place(relx=0.5 + 0.25, rely=0.5 + 0.35, anchor='center')

    # Espacio entre botones
    espacio_entre_botones = 30

    # Botón de Salir
    global boton_salir
    boton_salir = tk.Button(ventana_1, cursor="exchange", text="Regresar", height="4", width="30",
                            background="#0a0c3f", fg="white", font=fuente_retro_5, relief="raised",
                            borderwidth=10, command=volver_inicio_sesion)
    boton_salir.place(relx=0.5 - 0.25, rely=0.5 + 0.35, anchor='center')

    global boton_configuración
    boton_configuración = tk.Button(ventana_1, cursor="exchange", text="Configuración",
                                    background="#0a0c3f", fg="white", font=("System 18 bold"),
                                    relief="raised", command="")
    boton_configuración.pack()
    boton_configuración.place(x=0, y=0, height=40, width=200)

    # Mostrar la ventana principal
    ventana_1.mainloop()


configurar_partida()
