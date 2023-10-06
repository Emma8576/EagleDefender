import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pymysql
import json
import pygame

# Variables globales para las ventanas 
ventana_1 = None
ventana_2 = None
ventana_3 = None
ventana_como_Jugar = None
ventana_configuración = None
seleccion = None

#Variable global para control de nivel de volumen
pygame.init()
#Esta función leerá el valor del volumen guardado
def leer_volumen():
    with open('volumen.txt', 'r') as archivo:
        return float(archivo.read())
volumen = leer_volumen()


pygame.mixer.music.load('welcomeInterfaceFramesSprites/Sounds/mainSound1.mp3')
pygame.mixer.music.set_volume(volumen)
pygame.mixer.music.play()

#Se agrega imagen de fondo
def cargar_imagen_de_fondo(ventana, ruta_imagen):
    # Cargar la imagen de fondo
    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)

    # Crear una etiqueta para mostrar la imagen de fondo
    etiqueta_fondo = Label(ventana, image=imagen)
    etiqueta_fondo.image = imagen  # Mantener una referencia a la imagen
    etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Cubrir toda la ventana

def salir(): 
    inicio.destroy()
    try:
        global ventana_como_Jugar
        ventana_como_Jugar.destroy()
    except:
        print("")



def inicio_partida():
    global inicio
    inicio=tk.Tk()
    inicio.configure(cursor="star")
    cargar_imagen_de_fondo(inicio, "loginImages/fondo1.png")
    inicio.attributes("-fullscreen", True)

    fondo = tk.PhotoImage(file="welcomeInterfaceFramesSprites/SavedItems/bg.png")


    global boton_cerrar
    boton_cerrar=tk.Button(inicio, text="Salir", 
                 command=salir, 
                 fg="gray1",
                 bg="#9e2254",
                 relief="sunken",
             font=("System 35 bold"),
                 cursor="exchange")
    boton_cerrar.pack()     
    boton_cerrar.place(relx=0.5, rely=0.9, anchor="center")


    global boton_abrir
    boton_abrir=tk.Button(inicio, text="Iniciar",
                        command=menu_login,
                        fg="white",
                        bg="#FF9900",
                        relief="sunken",
                        font=("System 35 bold"),
                        cursor="exchange")
    boton_abrir.pack()     
    boton_abrir.place(relx=0.5, rely=0.5, anchor="center")



    etiqueta_retro2 = Label(inicio, text="Battle City", bg="#180546", fg="white", font="8-Bit 100")
    etiqueta_retro2.place(relx=0.5, rely=0.1, anchor="center")

    if config["idioma"] == "inglés":
        boton_cerrar.config(text="Leave Game")
        boton_abrir.config(text="Start Game")

    inicio.mainloop()
#Función ventana Login
def menu_login():
    global ventana_1, seleccion
    # Crear una instancia de la ventana principal
    ventana_1=Toplevel(inicio)
    
    # Cargar imagen de fondo en la ventana principal
    cargar_imagen_de_fondo(ventana_1, "loginImages/fondo1.png")
    ventana_1.attributes("-fullscreen", True)
    # Establecer el título de la ventana
    ventana_1.title("Bienvenidos")

    # Cargar icono de la ventana
    ventana_1.iconbitmap("loginImages/icon.ico")

    def como_Jugar():
        # Función para cerrar la ventana
        def cerrar_ventana():
            ventana_como_Jugar.destroy()



        # Texto de las instrucciones
        instrucciones = """
        Instrucciones del juego "Eagle Defender":

        1. Jugador 1:
           - Selecciona y coloca bloques de madera, concreto o acero alrededor del águila.
           - Una vez colocados los bloques, haz click en "Comenzar Juego".

        2. Jugador 2:
           Usa el tanque con las siguientes municiones:
             - Bombas: Destruyen bloques de madera y dañan bloques de concreto y acero.
             - Bolas de fuego: Queman bloques de madera y causan daño a bloques de concreto y acero.
             - Bolas de agua: un disparo destruye bloques de madera, dos bloques de concreto y
               con tres bloques de acero.
             - El juego durará el tiempo de una canción seleccionada por el jugador.
             - Gana jugador 1 si su aguila no es alcanzada, si la aguila recibe daño gana jugador 2.
             

        3. Objetivo:
           - Jugador 1: Protege el águila del ataque del Jugador 2.
           - Jugador 2: Intenta destruir los bloques y alcanzar el águila.

        4. ¡Diviértete y que gane el mejor!

        """
        if config["idioma"] == "inglés":
            instrucciones = """
                    "Eagle Defender" Game Instructions:

                    1. Player 1:
                       - Select and place blocks of wood, concrete, or steel around the eagle.
                       - Once the blocks are placed, click on "Start Game".

                    2. Player 2:
                       Use the tank with the following ammunition:
                         - Bombs: Destroy wood blocks and damage concrete and steel blocks.
                         - Fireballs: Burn wood blocks and cause damage to concrete and steel blocks.
                         - Water Balls: One shot destroys wood blocks, two concrete blocks, and
                           three steel blocks.
                         - The game will last the duration of a song selected by the player.
                         - Player 1 wins if their eagle is not hit; if the eagle is damaged, Player 2 wins.

                    3. Objective:
                       - Player 1: Protect the eagle from Player 2's attack.
                       - Player 2: Try to destroy the blocks and hit the eagle.

                    4. Have fun and may the best player win!

                    """

        # Crear la ventana
        global ventana_como_Jugar
        ventana_como_Jugar = tk.Tk()
        ventana_como_Jugar.title("Instrucciones - Eagle Defender")

        #cargar_imagen_de_fondo(ventana_como_Jugar, "loginImages/fondo1.png")


        # Etiqueta para mostrar las instrucciones
        label = tk.Label(ventana_como_Jugar, text=instrucciones, justify="left", font=("Arial", 12))
        label.pack(padx=20, pady=20)

        # Botón para cerrar la ventana
        boton_cerrar = tk.Button(ventana_como_Jugar, text="Cerrar", command=cerrar_ventana)
        boton_cerrar.pack(pady=10)

        # Iniciar el bucle principal de la ventana
        ventana_como_Jugar.mainloop()
    
    # Se añade la fuente retro en diversos tamaños
    global fuente_retro_3
    fuente_retro = ("8-Bit Operator+ 8", 100)
    fuente_retro_1 = ("8-Bit Operator+ 8", 50)
    fuente_retro_2 = ("8-Bit Operator+ 8", 20)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana_1, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5, anchor='center') 
    etiqueta_retro.pack()
    
    #Etiqueta de acceder al juego
    ancho_pantalla = ventana_1.winfo_screenwidth()
    global etiqueta
    etiqueta = Label(ventana_1, text="Acceder al juego", bg="#101654", fg="white", font=fuente_retro_1)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=200) 


    # Botón de Iniciar Sesión
    global boton_inicio
    boton_inicio = tk.Button(ventana_1,cursor="exchange", text="Iniciar Sesión", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=inicio_sesion)
    boton_inicio.place(relx=0.5, rely=0.5, anchor='center')

    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de Registrarse
    global boton_registrarse
    boton_registrarse = tk.Button(ventana_1,cursor="exchange", text="Registrarse", height="4", background="#0a0c3f", fg="white", width="30", font=fuente_retro_3, relief="raised", borderwidth=10, command=registro)
    boton_registrarse.place(relx=0.5, rely=0.5 + espacio_entre_botones/200, anchor='center')

    # Botón de Salir
    global boton_salir
    boton_salir = tk.Button(ventana_1,cursor="exchange", text="Salir", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=ventana_1.destroy)
    boton_salir.place(relx=0.5, rely=0.5 + 1 * espacio_entre_botones/100, anchor='center')


    global boton_configuración 
    boton_configuración = tk.Button(ventana_1,cursor="exchange", text="Configuración", background = "#0a0c3f", fg="white", font=("System 18 bold"), relief="raised", command=abrir_configuracion)
    boton_configuración.pack()
    boton_configuración.place(x=0, y=0, height=40, width=200)

    global boton_playlist
    boton_configuración = tk.Button(ventana_1, text="Playlist", background = "#0a0c3f", fg="white", font=("System 18 bold"), relief="raised", command=ventana_playlist)
    boton_configuración.pack()
    boton_configuración.place(x=0, y=728, height=40, width=200)

    global boton_comoJugar
    boton_comoJugar = tk.Button(ventana_1, cursor="exchange", text="Como Jugar", background="#0a0c3f",
                                    fg="white", font=("System 18 bold"), relief="raised", command=como_Jugar)
    boton_comoJugar.pack()
    boton_comoJugar.place(x=0, y=60, height=40, width=200)

    seleccion = tk.StringVar()

    if config["idioma"] == "inglés":
        etiqueta.config(text="Access the game")
        boton_inicio.config(text="Log in")
        boton_registrarse.config(text="Sign in")
        boton_salir.config(text="Leave")
        boton_configuración.config(text="Configuration")
        boton_comoJugar.config(text="How to play")




    # Mostrar la ventana principal
    ventana_1.mainloop()


    
def cargar_idioma():
    idioma = seleccion.get()
    if idioma == "español":
        etiqueta.config(text="Acceder al juego")
        boton_inicio.config(text="Iniciar Sesión")
        boton_registrarse.config(text="Registrarse")
        boton_salir.config(text="Salir")
        boton_configuración.config(text="Configuración")
        etiqueta_4.config(text="Configuración")
        label_configuracion.config(text="Selecciona el idioma:")
        opcion_español.config(text="Español")
        opcion_ingles.config(text="Inglés")
        boton_aceptar.config(text="Aceptar")
        boton1.config(text="Volver")
        boton2.config(text="Subir Volumen")
        boton3.config(text="Bajar Volumen")
        boton_abrir.config(text="Iniciar")
        boton_cerrar.config(text="Salir")
        boton_configuración.config(text="Configuración")

        config["idioma"] = "español"
    elif idioma == "inglés":
        etiqueta.config(text="Access the game")
        boton_inicio.config(text="Log in")
        boton_registrarse.config(text="Sign in")
        boton_salir.config(text="Leave")
        boton_configuración.config(text="Configuration")
        etiqueta_4.config(text="Configuration")
        label_configuracion.config(text="Select a language")
        opcion_español.config(text="Spanish")
        opcion_ingles.config(text="English")
        boton_aceptar.config(text="Accept")
        boton1.config(text="Go back")
        boton2.config(text="Volume up")
        boton3.config(text="Volume down")
        boton_abrir.config(text="Start Game")
        boton_cerrar.config(text="Leave Game")
        boton_configuración.config(text="Configuration")

        config["idioma"] = "inglés"
    with open("config.json", "w") as f:
        json.dump(config, f)

#####################################
# Funcion para la ventana de la playlist 

def ventana_playlist():
    global ventana_playlist, seleccion
    ventana_playlist = tk.Toplevel(ventana_1)
    ventana_playlist.attributes("-fullscreen", True)
    cargar_imagen_de_fondo(ventana_playlist, "loginImages/fondo1.png")
    
    global etiqueta_playlist
    ancho_pantalla = ventana_playlist.winfo_screenwidth()
    etiqueta_playlist = Label(ventana_playlist, text="Configuración", bg="#101654", fg="white", font=("System 30 bold"))

    etiqueta_retro2 = Label(ventana_playlist, text="Battle City", bg="#000030", font=("System 30 bold"), fg="white")
    etiqueta_retro2.place(relx=0.5, rely=0.5, anchor='center') 
    etiqueta_retro2.pack()
    
    def salir():
        ventana_playlist.destroy()

        
    #boton para devolverse al menu 
    boton_devolver_playlist = tk.Button(ventana_playlist, text="Volver", command=salir, fg="snow", bg="SkyBlue3", relief="sunken", font=("System 30 bold"), cursor="exchange")
    boton_devolver_playlist.pack()      
    boton_devolver_playlist.place(x=0, y=0, height=50, width=150)

###############################

# Función para abrir configuración
     
def abrir_configuracion():
    global ventana_configuracion, seleccion
    ventana_configuracion = tk.Toplevel(ventana_1)
    ventana_configuracion.attributes("-fullscreen", True)
    cargar_imagen_de_fondo(ventana_configuracion, "loginImages/fondo1.png")
    ventana_configuracion.configure(cursor="star")

    
    global etiqueta_4
    ancho_pantalla = ventana_configuracion.winfo_screenwidth()
    etiqueta_4 = Label(ventana_configuracion, text="Configuración", bg="#101654", fg="white", font=("System 30 bold"))

    etiqueta_retro2 = Label(ventana_configuracion, text="Battle City", bg="#000030", font=("System 70 bold"), fg="white")
    etiqueta_retro2.place(relx=0.5, rely=0.5, anchor='center') 
    etiqueta_retro2.pack()


    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta_4.winfo_reqwidth()) // 2
    etiqueta_4.place(x=x, y=120)

    global label_configuracion
    label_configuracion = tk.Label(ventana_configuracion, text="Selecciona el idioma:", bg="SkyBlue2", fg="white", font=("System 30 bold"))
    label_configuracion.place(x=600, y=240)

    seleccion.set(config["idioma"])
    opciones_idioma = [("Español", "español"), ("Inglés", "inglés")]

    global opcion_español
    opcion_español = tk.Radiobutton(ventana_configuracion, text="Español", variable=seleccion, value="español", bg="SkyBlue3", fg="white",font=("System 30 bold"))
    opcion_español.pack(anchor="w")
    opcion_español.place(x=700, y=300)

    global opcion_ingles
    opcion_ingles = tk.Radiobutton(ventana_configuracion, text="Inglés", variable=seleccion, value="inglés", bg="SkyBlue3", fg="white",font=("System 30 bold"))
    opcion_ingles.pack(anchor="w")
    opcion_ingles.place(x=700, y=370)

    global boton_aceptar
    boton_aceptar = tk.Button(ventana_configuracion,cursor="exchange", text="Aceptar", command=cargar_idioma, bg="SkyBlue3", fg="white",font=("System 20 bold"))
    boton_aceptar.pack()
    boton_aceptar.place(x=750, y=450)
    
    actualizar_idioma_configuracion()

    #Se define las funciones para controlar el volumen del juego.

    def guardar_volumen(volumen):
        with open('volumen.txt', 'w') as archivo:
            archivo.write(str(volumen))
    def subir_volumen():
        global volumen
        if volumen < 1.0:
            volumen = min(1.0, volumen + 0.1)
            print("Nivel de volumen es " + str(volumen))
            pygame.mixer.music.set_volume(volumen)
            guardar_volumen(volumen)

    def bajar_volumen():
        global volumen
        if volumen > 0.0:
            volumen = max(0.0, volumen - 0.1)
            print("Nivel de volumen es "+str(volumen))
            pygame.mixer.music.set_volume(volumen)
    def salir():
        ventana_configuracion.destroy()

    #Definicion de Botones para la ventana de configuración
    global boton1
    boton1 = tk.Button(ventana_configuracion, text="Volver", # Se configura el botón "Volver" de "Acerca de"
                 command=salir,
                 fg="snow",
                 bg="#0e083e",
                 relief="sunken",
                 font=("System 35 bold"),
                 cursor="exchange")
    boton1.pack()       #Se posiciona el botón "Volver"
    boton1.place(x=550, y=550, height=50, width=210)

    global boton2
    boton2 = tk.Button(ventana_configuracion,text="Subir Volumen",  # Se configura el botón "Volver" de "Acerca de"
                       command=subir_volumen,
                       fg="snow",
                       bg="SkyBlue3",
                       relief="sunken",
                       font=("System 30 bold"),
                       cursor="exchange")
    boton2.pack()  # Se posiciona el botón "Subir Volumen"
    boton2.place(x=280, y=300, height=50, width=300)

    global boton3
    boton3 = tk.Button(ventana_configuracion, text="Bajar Volumen",  # Se configura el botón "Volver" de "Acerca de"
                       command=bajar_volumen,
                       fg="snow",
                       bg="SkyBlue3",
                       relief="sunken",
                       font=("System 30 bold"),
                       cursor="exchange")
    boton3.pack()  # Se posiciona el botón "Baja Volumen"
    boton3.place(x=280, y=360, height=50, width=300)
    seleccion.set(config["idioma"])

    if config["idioma"] == "inglés":
        etiqueta_4.config(text="Configuration")
        label_configuracion.config(text="Select a language")
        opcion_español.config(text="Spanish")
        opcion_ingles.config(text="English")
        boton_aceptar.config(text="Accept")
        boton2.config(text="Volume up")
        boton3.config(text="Volumen down")
        boton1.config(text="Go back")



    ventana_configuracion.mainloop()


def actualizar_idioma_configuracion():
    if seleccion.get() == "español":
        etiqueta_4.config(text="Configuración")
        label_configuracion.config(text="Seleccione el idioma:")
        opcion_español.config(text="Español")
        opcion_ingles.config(text="Inglés")
        boton_aceptar.config(text="Aceptar")
    elif seleccion.get() == "inglés":
        etiqueta_4.config(text="Configuration")
        label_configuracion.config(text="Select a language")
        opcion_español.config(text="Spanish")
        opcion_ingles.config(text="English")
        boton_aceptar.config(text="Accept")



try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    config = {"idioma": "español"}



def volver_a_inicio():
    global ventana_configuración
    if ventana_configuración:
        ventana_configuración.withdraw()
    if ventana_1:
        ventana_1.deiconify()



#Funcion para cerrar el juego
def cerrar_juego():
    ventana_1.destroy()


    
# Función para mostrar la ventana de inicio de sesión
def inicio_sesion():
    global ventana_2, seleccion
    if ventana_1:
        ventana_1.withdraw()
    
    # Crear una instancia de la ventana secundaria
    ventana_2 = Toplevel(ventana_1)
    ventana_2.attributes("-fullscreen", True)
    ventana_2.configure(cursor="star")

    global etiqueta_2
    etiqueta_2 = Label(ventana_2, text="Inicio de sesión", bg="#101654", fg="white")    
    # Cargar imagen de fondo en la ventana principal
    cargar_imagen_de_fondo(ventana_2, "loginImages/fondo1.png") 
    
     # Se añade la fuente retro en diversos tamañosglobal ventana_configuracion, seleccion
    ventana_configuracion = tk.Toplevel(ventana_1)
    ventana_configuracion.configure(bg="black")

    label_configuracion = tk.Label(ventana_configuracion, text="Seleccione el idioma:", bg="black", fg="white")
    label_configuracion.pack()


    seleccion.set(config["idioma"])

    
    fuente_retro = ("8-Bit Operator+ 8", 100)
    fuente_retro_1 = ("8-Bit Operator+ 8", 50)
    fuente_retro_2 = ("8-Bit Operator+ 8", 25)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana_2, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5, anchor='center') 
    etiqueta_retro.pack()
    
    # Etiqueta para llamar a la ventana de recuperación de contraseña
    global etiqueta_enlace
    etiqueta_enlace = tk.Label(ventana_2, text="¿Olvidaste tu contraseña?", cursor="hand2", bg="#000232", fg="white")
    etiqueta_enlace.place(relx=0.6, rely=0.6)
    etiqueta_enlace.bind("<Button-1>", lambda event: recuperar_contrasena())
    
    # Etiqueta para llamar a la ventana de recuperación de contraseña
    global etiqueta_enlace2
    etiqueta_enlace2 = tk.Label(ventana_2, text="Crea tu cuenta", cursor="hand2", bg="#000232", fg="white")
    etiqueta_enlace2.place(relx=0.3 + 0.23, rely=0.6)
    etiqueta_enlace2.bind("<Button-1>", lambda event: registro())

    #Etiqueta de acceder al juego
    global etiqueta_1
    ancho_pantalla = ventana_2.winfo_screenwidth()
    etiqueta_1 = Label(ventana_2, text="Inicio de Sesión", bg="#101654", fg="white", font=fuente_retro_1)

    #Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta_1.winfo_reqwidth()) // 2
    etiqueta_1.place(x=x, y=150)

    global nombre_usuario_verif
    global contrasena_usuario_verif
    
    
    nombre_usuario_verif = StringVar() 
    contrasena_usuario_verif = StringVar()

    #Se agrega la etiqueta de usuario
    global etiquetaUsuario
    etiquetaUsuario = Label(ventana_2, text="Usuario", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)  
    
    #Se agrega la etiqueta de contraseña
    global etiquetaContrasena
    etiquetaContrasena = Label(ventana_2, text="Contraseña", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)


    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiquetaUsuario.winfo_reqwidth()) // 2
    etiquetaUsuario.place(x=x, y=250) 
    
    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiquetaContrasena.winfo_reqwidth()) // 2
    etiquetaContrasena.place(x=x, y=370) 
    
    # Obtener el ancho de la pantalla
    ancho_pantalla = ventana_2.winfo_screenwidth()

    # Calcular la posición x para centrar horizontalmente los campos de entrada
    x_entry = (ancho_pantalla) // 3.1
    
    
    # Espacio para llenar usuario
    nombre_usuario_verif = tk.StringVar()
    nombre_usuario_entry1 = tk.Entry(ventana_2, textvariable=nombre_usuario_verif, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    nombre_usuario_entry1.place(x=x_entry, y=300)

    # Espacio para llenar contraseña
    contrasena_usuario_verif = tk.StringVar()
    contrasena_usuario_entry1 = tk.Entry(ventana_2, textvariable=contrasena_usuario_verif, bg="#9e2254", fg="white", show="*", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    contrasena_usuario_entry1.place(x=x_entry, y=420)
    
    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de Iniciar sesión de la ventana inicio de sesión
    global boton_inicio_sesion
    boton_inicio_sesion = Button(ventana_2, text="Iniciar Sesión", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=validar_datos)
    boton_inicio_sesion.place(relx=0.5, rely=0.7, anchor='center')
    
        # Botón de Atrás de la ventana inicio de sesión
    global botonAtras
    botonAtras = Button(ventana_2, text="Atrás", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=volver_atras)
    botonAtras.place(relx=0.5, rely=0.5 + 1 * espacio_entre_botones/90, anchor='center')


    ventana_2.protocol("WM_DELETE_WINDOW", volver_atras)  # Manejar cierre de ventana

    if config["idioma"] == "inglés":
        etiqueta_1.config(text="Log in")
        etiqueta_enlace.config(text="Forgot password?")
        etiqueta_enlace2.config(text="Create account")
        etiquetaUsuario.config(text="User")
        etiquetaContrasena.config(text="Password")
        boton_inicio_sesion.config(text="Log in")
        botonAtras.config(text="Go back")
    
    ventana_2.mainloop()

#Función ventana de Registro
def registro():
    global ventana_3, seleccion
    if ventana_1:
        ventana_1.withdraw()
    
    # Crear una instancia de la ventana secundaria
    ventana_3 = Toplevel(ventana_1)
    ventana_3.attributes("-fullscreen", True)
    ventana_3.title("Registro")
    ventana_3.configure(cursor="star")
    
    # Cargar imagen de fondo en la ventana principal
    cargar_imagen_de_fondo(ventana_3, "loginImages/fondo1.png") 
    
     # Se añade la fuente retro en diversos tamaños
    fuente_retro = ("8-Bit Operator+ 8", 100)
    fuente_retro_1 = ("8-Bit Operator+ 8", 50)
    fuente_retro_2 = ("8-Bit Operator+ 8", 25)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    seleccion.set(config["idioma"])
    # Etiqueta para llamar a la ventana de recuperación de contraseña
    global etiqueta_enlace
    etiqueta_enlace = tk.Label(ventana_3, text="¿Iniciar Sesión?", cursor="hand2", bg="#000232", fg="white")
    etiqueta_enlace.place(relx=0.6 + 0.04, rely=0.3 + 0.09)
    etiqueta_enlace.bind("<Button-1>", lambda event: inicio_sesion())

    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana_3, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.7, anchor='center') 
    etiqueta_retro.pack()
    
    #Etiqueta de registro del juego
    global etiqueta3
    ancho_pantalla = ventana_3.winfo_screenwidth()
    etiqueta3 = Label(ventana_3, text="Registrarse", bg="#101654", fg="white", font=fuente_retro_1)


    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta3.winfo_reqwidth()) // 2
    etiqueta3.place(x=x, y=120)
    
    #variables para almacenar los datos ingresados por el usuario
    nombre_usuario_verif1 = StringVar() 
    contrasena_usuario_verif1 = StringVar()
    correoUsuario_verif = StringVar()

    #Se agrega la etiqueta de usuario
    global etiquetaUsuario
    etiquetaUsuario = Label(ventana_3, text="Usuario", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)  
    
    #Se agrega la etiqueta de contraseña
    global etiquetaContrasena
    etiquetaContrasena = Label(ventana_3, text="Contraseña", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
    #Se agrega la etiqueta del correo
    global etiquetaCorreo
    etiquetaCorreo = Label(ventana_3, text="Correo", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
    # Calcula la posición x para que la etiqueta usuario esté en el centro horizontal
    x = (ancho_pantalla - etiquetaUsuario.winfo_reqwidth()) // 2
    etiquetaUsuario.place(x=x, y=200) 
    
    # Calcula la posición x para que la etiqueta  contraseña esté en el centro horizontal
    x = (ancho_pantalla - etiquetaContrasena.winfo_reqwidth()) // 2
    etiquetaContrasena.place(x=x, y=310) 
    
    # Calcula la posición x para que la etiqueta correo esté en el centro horizontal
    x = (ancho_pantalla - etiquetaCorreo.winfo_reqwidth()) // 2
    etiquetaCorreo.place(x=x, y=420) 
    
    # Obtener el ancho de la pantalla
    ancho_pantalla = ventana_3.winfo_screenwidth()

    # Calcular la posición x para centrar horizontalmente los campos de entrada
    x_entry = (ancho_pantalla) // 3.1
    
    global nombre_usuario_entry
    global contrasena_usuario_entry
    global correo_usuario_entry
    
    # Espacio para llenar usuario
    nombre_usuario_verif1 = tk.StringVar()
    nombre_usuario_entry = tk.Entry(ventana_3, textvariable=nombre_usuario_verif1, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    nombre_usuario_entry.place(x=x_entry, y=250)

    # Espacio para llenar contraseña
    contrasena_usuario_verif = tk.StringVar()
    contrasena_usuario_entry = tk.Entry(ventana_3, textvariable=contrasena_usuario_verif, bg="#9e2254", fg="white", show="*", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    contrasena_usuario_entry.place(x=x_entry, y=360)
    
    #Espacio para llenar contraseña
    correoUsuario_verif = tk.StringVar()
    correo_usuario_entry = tk.Entry(ventana_3, textvariable=correoUsuario_verif, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    correo_usuario_entry.place(x=x_entry, y=470)
    
    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de registrarse de la ventana de registro
    global boton_registro
    boton_registro = Button(ventana_3, text="Registrar", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command= verificar_contraseña)
    boton_registro.place(relx=0.5, rely=0.8, anchor='center')
    
    # Botón de Atrás de la ventana inicio de sesión
    global botonAtras
    botonAtras = Button(ventana_3, text="Atrás", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=volver_atras)
    botonAtras.place(relx=0.5, rely=0.6 + 1 * espacio_entre_botones/90, anchor='center')


    ventana_3.protocol("WM_DELETE_WINDOW", volver_atras)  # Manejar cierre de ventana

    if config["idioma"] == "inglés":
        etiqueta_enlace.config(text="Log in?")
        etiqueta3.config(text="Sign in")
        etiquetaUsuario.config(text="User")
        etiquetaContrasena.config(text="Password")
        etiquetaCorreo.config(text="Email")
        boton_registro.config(text="Register")
        botonAtras.config(text="Back")
  
    ventana_3.mainloop()

#Función para establecer logitud de 8 caracteres a la contraseña
def verificar_contraseña():
    global config
    contrasena = contrasena_usuario_entry.get()
    if len(contrasena) >= 8:
        insertar_datos()
        
        #Eliminar el contenido de los campos una vez se haya completado el registro
        nombre_usuario_entry.delete(0,END)
        correo_usuario_entry.delete(0,END)
        contrasena_usuario_entry.delete(0,END)
        
        # Botón de registrarse de la ventana de registro
        global boton_inicio_sesion
        boton_inicio_sesion = Button(ventana_3, text="Iniciar sesión", height="3", width="15", background="#ffa181", fg="black", font=fuente_retro_3, relief="raised", borderwidth=10, command=inicio_sesion)
        boton_inicio_sesion.place(relx=0.9 + 0.02, rely=0.1 - 0.03, anchor='center')
    else:
        global messagebox
        if config["idioma"] == "inglés":
            messagebox.showerror(title="Aviso", message="Password must have at least 8 characters")
        else:
            messagebox.showerror(title="Aviso", message="La contraseña debe tener almenos 8 caracteres")


#función interfaz para recuperar contraseña
def recuperar_contrasena():
    global ventana_4, seleccion
    if ventana_1:
        ventana_1.withdraw()
    
    # Crear una instancia de la ventana secundaria
    ventana_4 = Toplevel(ventana_1)
    ventana_4.attributes("-fullscreen", True)
    ventana_4.title("Recuperar contraseña")
    
    # Cargar imagen de fondo en la ventana principal
    cargar_imagen_de_fondo(ventana_4, "loginImages/fondo1.png") 

    seleccion.set(config["idioma"])
    
     # Se añade la fuente retro en diversos tamaños
    fuente_retro = ("8-Bit Operator+ 8", 100)
    fuente_retro_1 = ("8-Bit Operator+ 8", 40)
    fuente_retro_2 = ("8-Bit Operator+ 8", 25)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    seleccion.set(config["idioma"])
    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana_4, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5 + 0.05, anchor='center') 
    etiqueta_retro.pack()
    
    #Etiqueta de registro del juego
    global etiqueta_4
    ancho_pantalla = ventana_4.winfo_screenwidth()
    etiqueta_4 = Label(ventana_4, text="Cambia tu contraseña", bg="#101654", fg="white", font=fuente_retro_1)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta_4.winfo_reqwidth()) // 2
    etiqueta_4.place(x=x, y=105)
    
    #variables para almacenar los datos ingresados por el usuario
    nombreUsuarioOCorreo_verif = StringVar() 

    #Se agrega la etiqueta de usuario
    global etiqueta_usuario2
    etiqueta_usuario2 = Label(ventana_4, text="Usuario", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)  
     
    #Se agrega la etiqueta del correo
    global etiqueta_correo2
    etiqueta_correo2 = Label(ventana_4, text="Correo", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
     
    #Se agrega la etiqueta de contraseña
    global etiqueta_contrasena2
    etiqueta_contrasena2 = Label(ventana_4, text="Nueva Contraseña", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
    #Se agrega la etiqueta de confirmar contraseña
    global etiqueta_contrasena_re
    etiqueta_contrasena_re = Label(ventana_4, text="Confirmar Contraseña", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)

    
    # Calcula la posición x para que la etiqueta usuario esté en el centro horizontal
    x = (ancho_pantalla - etiqueta_usuario2.winfo_reqwidth()) // 2
    etiqueta_usuario2.place(x=x, y=190) 
    
        # Calcula la posición x para que la etiqueta correo esté en el centro horizontal
    x = (ancho_pantalla - etiqueta_correo2.winfo_reqwidth()) // 2
    etiqueta_correo2.place(x=x, y=290) 
    
        # Calcula la posición x para que la etiqueta contraseña esté en el centro horizontal
    x = (ancho_pantalla - etiqueta_contrasena2.winfo_reqwidth()) // 2
    etiqueta_contrasena2.place(x=x, y=390) 
    
        # Calcula la posición x para que la etiqueta repetir contraseña esté en el centro horizontal
    x = (ancho_pantalla - etiqueta_contrasena_re.winfo_reqwidth()) // 2
    etiqueta_contrasena_re.place(x=x, y=490) 
    
    # Obtener el ancho de la pantalla
    ancho_pantalla = ventana_4.winfo_screenwidth()

    # Calcular la posición x para centrar horizontalmente los campos de entrada
    x_entry = (ancho_pantalla) // 3.4
    
    global nombre_usuario2_entry
    global correo_entry
    global contrasena_entry
    global contrasena_Re_entry

    # Espacio para llenar usuario
    nombre_usuario_verif2 = tk.StringVar()
    nombre_usuario2_entry = tk.Entry(ventana_4, textvariable=nombre_usuario_verif2, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    nombre_usuario2_entry.place(x=x_entry, y=235)
    
    # Espacio para llenar correo
    correo_verif2 = tk.StringVar()
    correo_entry = tk.Entry(ventana_4, textvariable=correo_verif2, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    correo_entry.place(x=x_entry, y=335)
    
    # Espacio para llenar contraseña
    contrasena_verif2 = tk.StringVar()
    contrasena_entry = tk.Entry(ventana_4, textvariable=contrasena_verif2, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    contrasena_entry.place(x=x_entry, y=435)
    
    # Espacio para llenar contraseña repetida
    contrasena_Re_verif2 = tk.StringVar()
    contrasena_Re_entry = tk.Entry(ventana_4, textvariable=contrasena_Re_verif2, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    contrasena_Re_entry.place(x=x_entry, y=535)
    
    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de registrarse de la ventana de registro
    global boton_registro2
    boton_registro2 = Button(ventana_4, text="Guardar cambios", height="3", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=actualiza_contraseña)
    boton_registro2.place(relx=0.5, rely=0.8 + 0.03, anchor='center')
    
    # Botón de Atrás de la ventana inicio de sesión
    global boton_atras2
    boton_atras2 = Button(ventana_4, text="Atrás", height="3", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=volver_atras)
    boton_atras2.place(relx=0.5, rely=0.6 + 1 * espacio_entre_botones/90, anchor='center')


    ventana_4.protocol("WM_DELETE_WINDOW", volver_atras)  # Manejar cierre de ventana
    
    if config["idioma"] == "inglés":
        etiqueta_4.config(text="Change your password")
        etiqueta_usuario2.config(text="User")
        etiqueta_correo2.config(text="Email")
        etiqueta_contrasena2.config(text="New Password")
        etiqueta_contrasena_re.config(text="Confirm password")
        boton_registro2.config(text="Save changes")
        boton_atras2.config(text="Back")

    ventana_4.mainloop()

# Función para volver atrás
def volver_atras():
    global ventana_2
    if ventana_2:
        ventana_2.withdraw()
    if ventana_1:
        ventana_1.deiconify()

"*******************************************************/Conexiones y modificaciones con base de datos************************************************************"

def insertar_datos():
    global config
    #Conexión con la base de datos local
    bd = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="bd1"
    )
    f_cursor=bd.cursor()
    # Definición de la consulta SQL para INSERT
    sql = "INSERT INTO login (Correo, Usuario, Contrasena) VALUES ('{0}', '{1}', '{2}')".format(correo_usuario_entry.get(), nombre_usuario_entry.get(), contrasena_usuario_entry.get())
    
    try:
        f_cursor.execute(sql)
        bd.commit()
        if config["idioma"] == "inglés":
            messagebox.showinfo(message="You have been registered successfully. Please log in to start the game", title="Aviso")
        else:
            messagebox.showinfo(message="Has sido registrado correctamente. Inicia sesión para empezar el juego", title="Aviso")
    except:
        bd.rollback()
        if config["idioma"] == "inglés":
            messagebox.showerror(message="Your registration could not be completed", title="Aviso")
        else:
            messagebox.showerror(message="Tu registro no se pudo completar", title="Aviso")
    
    bd.close()

#Validar datos de ingreso
def validar_datos():
    global config
        #Conexión con la base de datos local
    bd = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="bd1"
    )
    f_cursor = bd.cursor()
    #Verifica el inicio de sesión correcto o incorrecto.
    f_cursor.execute("SELECT Contrasena FROM login WHERE usuario='"+nombre_usuario_verif.get()+"' and contrasena= '"+contrasena_usuario_verif.get()+"'")
    if f_cursor.fetchall():
        if config["idioma"] == "inglés":
            messagebox.showinfo(title="Successful login",message="Usuario y Contraseña correcta")
                    # boton de playlist
            global boton_playlist
            boton_playlist = tk.Button(ventana_1, text="Playlist", background="#0a0c3f", fg="white", font=("System 18 bold"), relief="raised", command=ventana_playlist)
            boton_playlist.pack()
            boton_playlist.place(x=0, y=729, height=40, width=200)
        else:
            messagebox.showinfo(title="Inicio de sesión exitoso",message="Usuario y Contraseña correcta")
    else:
        messagebox.showerror(title="Inicio de sesión incorrecto",message="Usuario o Contraseña incorrecta")
    bd.close()

##################### LA PLAYLIST ############################

def ventana_playlist():
    global ventana_playlist
    ventana_playlist = tk.Toplevel(ventana_1)
    ventana_playlist.attributes("-fullscreen", True)
    cargar_imagen_de_fondo(ventana_playlist, "loginImages/fondo1.png")
    
    #Conexión con la base de datos local
    bd = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="bd1")
    
    texto2 =tk.Label(ventana_playlist, text="Por favor ingrese cinco canciones:") #Botón para ir al menú
    texto2.place(x = 370, y = 50) #Posición 
    texto2.config(width="27", height="1")#letra
    texto2.config(font=("System 30 bold"))#
    texto2.config(bg="#F4BFAD")#Color de fondo
    texto2.config(fg="#000A24")
    texto2.config(relief="raised", borderwidth=10)
    
    #boton para devolverse al menu 
    boton_devolver_playlist = tk.Button(ventana_playlist, text="Volver", command=salir, fg="snow", bg="SkyBlue3", relief="sunken", font=("System 30 bold"), cursor="exchange")
    boton_devolver_playlist.pack()      
    boton_devolver_playlist.place(x=0, y=0, height=50, width=150)
    
    # Cuadro de texto para ingresar el nombre de usuario
    cuadro_usuario = tk.Entry(ventana_playlist)
    cuadro_usuario.place(x=370, y=350)

    # Cuadro de texto para ingresar las canciones
    cuadro_canciones = tk.Text(ventana_playlist, height=5, width=30)
    cuadro_canciones.place(x=370, y=400)

    # Botón para guardar las canciones y el nombre de usuario en la base de datos
    boton_guardar = tk.Button(ventana_playlist, text="Guardar", command=lambda: guardar_canciones(bd, cuadro_usuario, cuadro_canciones))
    boton_guardar.place(x=370, y=500)

def guardar_canciones(bd, cuadro_usuario, cuadro_canciones):
    nombre_usuario = cuadro_usuario.get()  # Obtén el nombre de usuario del cuadro de texto
    canciones = cuadro_canciones.get("1.0", "end-1c")  # Obtiene el texto del cuadro de texto de canciones

    # Crea una instancia de cursor y ejecuta la inserción en la base de datos
    cursor = bd.cursor()
    cursor.execute("INSERT INTO canciones (usuario, canciones) VALUES (%s, %s)", (nombre_usuario, canciones))
    bd.commit()

    # Cierra la conexión a la base de datos
    bd.close()


def salir():
    ventana_playlist.destroy() 
            
######################################## TERMINA LO DE LA PLAYLIST ######################




######################################## CALIFICAR ###################################
def actualiza_contraseña():
    global config
    # Verifica que todos los campos estén llenos
    if nombre_usuario2_entry.get() == '' or correo_entry.get() == '' or contrasena_entry.get() == '' or contrasena_Re_entry.get() == '':
        if config["idioma"] == "inglés":
            messagebox.showerror(title="Aviso", message="All fields must be filled in")
        else:
            messagebox.showerror(title="Aviso", message="Todos los campos deben estar llenos")
        return

    # Verifica que las contraseñas ingresadas sean iguales
    elif contrasena_entry.get() != contrasena_Re_entry.get():
        if config["idioma"] == "inglés":
            messagebox.showerror(title="Alerta", message="The entered passwords do not match")
        else:
            messagebox.showerror(title="Alerta", message="Las contraseñas ingresadas no coinciden")
        return
    else:
        # Conexión con la base de datos local
        bd = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db="bd1"
        )

        # Crear un cursor para ejecutar consultas SQL
        f_cursor = bd.cursor()

        # Consulta para verificar si el correo está registrado
        consulta = 'SELECT * FROM login WHERE Correo=%s'
        f_cursor.execute(consulta, (correo_entry.get()))

        # Recuperar la primera fila de resultados
        row = f_cursor.fetchone()
        
        # Verificar si el correo no está registrado
        if row is None:
            if config["idioma"] == "inglés":
                messagebox.showerror(title="Alert", message="The entered email is not registered, please use the email used for registration")
            else:
                messagebox.showerror(title="Alerta", message="El correo ingresado no está registrado, utilice el correo con el que realizó el registro")
            return

        else:
            # Consulta para actualizar la contraseña en la base de datos
            consulta = 'UPDATE login SET Contrasena=%s WHERE Correo=%s'
            f_cursor.execute(consulta, (contrasena_Re_entry.get(), correo_entry.get()))
            
            # Confirmar los cambios en la base de datos
            bd.commit()
            
            # Cerrar la conexión a la base de datos
            bd.close()
            
            # Mostrar un mensaje informativo de éxito
            if config["idioma"] == "inglés":
                messagebox.showinfo(title="Notice", message="Your password has been successfully changed. Please return to the login screen to continue.")
            else:
                messagebox.showinfo(title="Aviso", message="Su contraseña ha sido cambiada con éxito, vuelva al inicio de sesión para continuar")
            #Eliminar el contenido de los campos una vez se haya completado el cambio de contraseña
            nombre_usuario2_entry.delete(0,END)
            correo_entry.delete(0,END)
            contrasena_entry.delete(0,END)
            contrasena_Re_entry.delete(0,END)

            # Botón de registrarse de la ventana de registro
            boton_inicio_sesion = Button(ventana_4, text="Iniciar sesión", height="3", width="15", background="#ffa181", fg="black", font=fuente_retro_3, relief="raised", borderwidth=10, command=inicio_sesion)
            boton_inicio_sesion.place(relx=0.9 + 0.02, rely=0.1 - 0.03, anchor='center')
            
    def ventana_ingreso_cancion():
        #boton para entrar a ingresar las canciones 
        global boton_configuración 
        boton_configuración = tk.Button(ventana_1, text="Playlist", background = "#0a0c3f", fg="white", font=("System 18 bold"), relief="raised", command=abrir_configuracion)
        boton_configuración.pack()
        boton_configuración.place(x=0, y=0, height=40, width=200)

        


inicio_partida()
#LOS MILTONEANOS