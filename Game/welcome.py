import pygame
from pygame import *
import sys
import time
import tkinter as tk
import os
import msvcrt
import subprocess

init()
screen_info = display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

screen = display.set_mode((screen_width, screen_height), FULLSCREEN)
window = tk.Tk()

volumen = 1.0


def iniciar():
    pygame.mixer.music.load('welcomeInterfaceFramesSprites/Sounds/mainSound1.mp3')
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1)


# Iniciar automáticamente la configuración de volumen al ejecutar el juego
iniciar()

images = []
close = []

# Programar sprites ventana central
for i in range(1, 7):
    name = "welcomeInterfaceFramesSprites/mainItems/frame-"+str(i)+" (Custom).gif"
    images.append(image.load(name))

for i in range(1, 11):
    name1 = "welcomeInterfaceFramesSprites/mainItems1/frame-"+str(i)+".png"
    close.append(image.load(name1))

def abrir_login():
    ventana1 = None
ventana2 = None
ventana3 = None
ventana_de_figuración = None


#Se agrega imagen de fondo
def cargar_imagen_de_fondo(ventana, ruta_imagen):
    # Cargar la imagen de fondo
    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)

    # Crear una etiqueta para mostrar la imagen de fondo
    etiqueta_fondo = Label(ventana, image=imagen)
    etiqueta_fondo.image = imagen  # Mantener una referencia a la imagen
    etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Cubrir toda la ventana

    
def menu_login():
    global ventana1
    # Crear una instancia de la ventana principal
    ventana1 = tk.Tk()
    ventana1.attributes("-fullscreen", True)
    
    # Cargar imagen de fondo en la ventana principal
    cargar_imagen_de_fondo(ventana1, "loginImages/fondo1.png")
    
    # Establecer el título de la ventana
    ventana1.title("Bienvenidos")

    # Cargar icono de la ventana
    ventana1.iconbitmap("loginImages/icon.ico")

    
    # Se añade la fuente retro en diversos tamaños
    fuente_retro = ("8-Bit Operator+ 8", 100)
    fuente_retro_1 = ("8-Bit Operator+ 8", 50)
    fuente_retro_2 = ("8-Bit Operator+ 8", 20)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana1, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5, anchor='center') 
    etiqueta_retro.pack()
    
    #Etiqueta de acceder al juego
    ancho_pantalla = ventana1.winfo_screenwidth()
    etiqueta = Label(ventana1, text="Acceder al juego", bg="#101654", fg="white", font=fuente_retro_1)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=200) 


    # Botón de Iniciar Sesión
    botonInicio = tk.Button(ventana1, text="Iniciar Sesión", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=inicio_sesion)
    botonInicio.place(relx=0.5, rely=0.5, anchor='center')

    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de Registrarse
    botonRegistrarse = tk.Button(ventana1, text="Registrarse", height="4", background="#0a0c3f", fg="white", width="30", font=fuente_retro_3, relief="raised", borderwidth=10, command=registro)
    botonRegistrarse.place(relx=0.5, rely=0.5 + espacio_entre_botones/200, anchor='center')

    # Botón de Salir
    botonSalir = tk.Button(ventana1, text="Salir", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=ventana1.destroy)
    botonSalir.place(relx=0.5, rely=0.5 + 1 * espacio_entre_botones/100, anchor='center')

    botonConfiguración = tk.Button(ventana1, text="Configuración", background = "#0a0c3f", fg="white", font=("System 18 bold"), relief="raised", command=abrir_configuracion)
    botonConfiguración.pack()
    botonConfiguración.place(x=0, y=0, height=40, width=200)


    # Mostrar la ventana principal
    ventana1.mainloop()



def abrir_configuracion():
    global ventana_de_figuración
    if ventana1:
        ventana1.withdraw()

    ventana_de_figuración = tk.Toplevel(ventana1)
    ventana_de_figuración.wm_attributes('-fullscreen', '1') 

    cargar_imagen_de_fondo(ventana_de_figuración, "loginImages/fondo1.png")

    botonVolver = tk.Button(ventana_de_figuración, text="Volver", height="4", width="30", background="#0a0c3f", font=("System 18 bold"),fg="white", relief="raised", command=volver_a_inicio)
    botonVolver.place(x=0, y=0, height=40, width=200)

    ventana_de_figuración.protocol("WM_DELETE_WINDOW", volver_a_inicio)
    ventana_de_figuración.mainloop()

def volver_a_inicio():
    global ventana_de_figuración
    if ventana_de_figuración:
        ventana_de_figuración.withdraw()
    if ventana1:
        ventana1.deiconify()






#Funcion para cerrar el juego
def cerrarJuego():
    ventana1.destroy()
    
# Función para mostrar la ventana de inicio de sesión
def inicio_sesion():
    global ventana2
    if ventana1:
        ventana1.withdraw()
    
    # Crear una instancia de la ventana secundaria
    ventana2 = Toplevel(ventana1)
    ventana2.attributes("-fullscreen", True)
    ventana2.title("Iniciar sesión")
    
    # Cargar imagen de fondo en la ventana principal
    cargar_imagen_de_fondo(ventana2, "loginImages/fondo1.png") 
    
     # Se añade la fuente retro en diversos tamaños
    fuente_retro = ("8-Bit Operator+ 8", 100)
    fuente_retro_1 = ("8-Bit Operator+ 8", 50)
    fuente_retro_2 = ("8-Bit Operator+ 8", 25)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana2, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5, anchor='center') 
    etiqueta_retro.pack()
    
    # Etiqueta para llamar a la ventana de recuperación de contraseña
    etiqueta_enlace = tk.Label(ventana2, text="¿Olvidaste tu contraseña?", cursor="hand2", bg="#000232", fg="white")
    etiqueta_enlace.place(relx=0.6, rely=0.6)
    etiqueta_enlace.bind("<Button-1>", lambda event: recuperar_contrasena())
    
    # Etiqueta para llamar a la ventana de recuperación de contraseña
    etiqueta_enlace2 = tk.Label(ventana2, text="Crea tu cuenta", cursor="hand2", bg="#000232", fg="white")
    etiqueta_enlace2.place(relx=0.3 + 0.23, rely=0.6)
    etiqueta_enlace2.bind("<Button-1>", lambda event: registro())

    #Etiqueta de acceder al juego
    ancho_pantalla = ventana2.winfo_screenwidth()
    etiqueta = Label(ventana2, text="Inicio de Sesión", bg="#101654", fg="white", font=fuente_retro_1)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=150)

    global nombreUsuario_verif
    global contrasenaUsuario_verif
    
    
    nombreUsuario_verif = StringVar() 
    contrasenaUsuario_verif = StringVar()

    #Se agrega la etiqueta de usuario
    etiquetaUsuario = Label(ventana2, text="Usuario", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)  
    
    #Se agrega la etiqueta de contraseña
    etiquetaContrasena = Label(ventana2, text="Contraseña", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiquetaUsuario.winfo_reqwidth()) // 2
    etiquetaUsuario.place(x=x, y=250) 
    
    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiquetaContrasena.winfo_reqwidth()) // 2
    etiquetaContrasena.place(x=x, y=370) 
    
    # Obtener el ancho de la pantalla
    ancho_pantalla = ventana2.winfo_screenwidth()

    # Calcular la posición x para centrar horizontalmente los campos de entrada
    x_entry = (ancho_pantalla) // 3.1
    
    
    # Espacio para llenar usuario
    nombreUsuario_verif = tk.StringVar()
    nombre_usuario_entry1 = tk.Entry(ventana2, textvariable=nombreUsuario_verif, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    nombre_usuario_entry1.place(x=x_entry, y=300)

    # Espacio para llenar contraseña
    contrasenaUsuario_verif = tk.StringVar()
    contrasena_usuario_entry1 = tk.Entry(ventana2, textvariable=contrasenaUsuario_verif, bg="#9e2254", fg="white", show="*", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    contrasena_usuario_entry1.place(x=x_entry, y=420)
    
    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de Iniciar sesión de la ventana inicio de sesión
    botonInicioSesion = Button(ventana2, text="Iniciar Sesión", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=validar_datos)
    botonInicioSesion.place(relx=0.5, rely=0.7, anchor='center')
    
        # Botón de Atrás de la ventana inicio de sesión
    botonAtras = Button(ventana2, text="Atrás", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=volver_atras)
    botonAtras.place(relx=0.5, rely=0.5 + 1 * espacio_entre_botones/90, anchor='center')


    ventana2.protocol("WM_DELETE_WINDOW", volver_atras)  # Manejar cierre de ventana
    
    ventana2.mainloop()

#Función ventana de Registro
def registro():
    global ventana3
    if ventana1:
        ventana1.withdraw()
    
    # Crear una instancia de la ventana secundaria
    ventana3 = Toplevel(ventana1)
    ventana3.attributes("-fullscreen", True)
    ventana3.title("Registro")
    
    # Cargar imagen de fondo en la ventana principal
    cargar_imagen_de_fondo(ventana3, "loginImages/fondo1.png") 
    
     # Se añade la fuente retro en diversos tamaños
    fuente_retro = ("8-Bit Operator+ 8", 100)
    fuente_retro_1 = ("8-Bit Operator+ 8", 50)
    fuente_retro_2 = ("8-Bit Operator+ 8", 25)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    # Etiqueta para llamar a la ventana de recuperación de contraseña
    etiqueta_enlace = tk.Label(ventana3, text="¿Iniciar Sesión?", cursor="hand2", bg="#000232", fg="white")
    etiqueta_enlace.place(relx=0.6 + 0.04, rely=0.3 + 0.09)
    etiqueta_enlace.bind("<Button-1>", lambda event: inicio_sesion())

    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana3, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.7, anchor='center') 
    etiqueta_retro.pack()
    
    #Etiqueta de registro del juego
    ancho_pantalla = ventana3.winfo_screenwidth()
    etiqueta = Label(ventana3, text="Registrarse", bg="#101654", fg="white", font=fuente_retro_1)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=120)
    
    #variables para almacenar los datos ingresados por el usuario
    nombreUsuario_verif1 = StringVar() 
    contrasenaUsuario_verif1 = StringVar()
    correoUsuario_verif = StringVar()

    #Se agrega la etiqueta de usuario
    etiquetaUsuario = Label(ventana3, text="Usuario", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)  
    
    #Se agrega la etiqueta de contraseña
    etiquetaContrasena = Label(ventana3, text="Contraseña", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
    #Se agrega la etiqueta del correo
    etiquetaCorreo = Label(ventana3, text="Correo", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
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
    ancho_pantalla = ventana3.winfo_screenwidth()

    # Calcular la posición x para centrar horizontalmente los campos de entrada
    x_entry = (ancho_pantalla) // 3.1
    
    global nombre_usuario_entry
    global contrasena_usuario_entry
    global correo_usuario_entry
    
    # Espacio para llenar usuario
    nombreUsuario_verif1 = tk.StringVar()
    nombre_usuario_entry = tk.Entry(ventana3, textvariable=nombreUsuario_verif1, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    nombre_usuario_entry.place(x=x_entry, y=250)

    # Espacio para llenar contraseña
    contrasenaUsuario_verif = tk.StringVar()
    contrasena_usuario_entry = tk.Entry(ventana3, textvariable=contrasenaUsuario_verif, bg="#9e2254", fg="white", show="*", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    contrasena_usuario_entry.place(x=x_entry, y=360)
    
    #Espacio para llenar contraseña
    correoUsuario_verif = tk.StringVar()
    correo_usuario_entry = tk.Entry(ventana3, textvariable=correoUsuario_verif, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=22)
    correo_usuario_entry.place(x=x_entry, y=470)
    
    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de registrarse de la ventana de registro
    botonRegistro = Button(ventana3, text="Registrar", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=insertar_datos)
    botonRegistro.place(relx=0.5, rely=0.8, anchor='center')
    
    # Botón de Atrás de la ventana inicio de sesión
    botonAtras = Button(ventana3, text="Atrás", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=volver_atras)
    botonAtras.place(relx=0.5, rely=0.6 + 1 * espacio_entre_botones/90, anchor='center')


    ventana3.protocol("WM_DELETE_WINDOW", volver_atras)  # Manejar cierre de ventana
    
    ventana3.mainloop()

#función interfaz para recuperar contraseña
def recuperar_contrasena():
    global ventana4
    if ventana1:
        ventana1.withdraw()
    
    # Crear una instancia de la ventana secundaria
    ventana4 = Toplevel(ventana1)
    ventana4.attributes("-fullscreen", True)
    ventana4.title("Recuperar contraseña")
    
    # Cargar imagen de fondo en la ventana principal
    cargar_imagen_de_fondo(ventana4, "loginImages/fondo1.png") 
    
     # Se añade la fuente retro en diversos tamaños
    fuente_retro = ("8-Bit Operator+ 8", 100)
    fuente_retro_1 = ("8-Bit Operator+ 8", 40)
    fuente_retro_2 = ("8-Bit Operator+ 8", 25)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana4, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5 + 0.05, anchor='center') 
    etiqueta_retro.pack()
    
    #Etiqueta de registro del juego
    ancho_pantalla = ventana4.winfo_screenwidth()
    etiqueta = Label(ventana4, text="Cambia tu contraseña", bg="#101654", fg="white", font=fuente_retro_1)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=105)
    
    #variables para almacenar los datos ingresados por el usuario
    nombreUsuarioOCorreo_verif = StringVar() 

    #Se agrega la etiqueta de usuario
    etiquetaUsuario = Label(ventana4, text="Usuario", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)  
     
    #Se agrega la etiqueta del correo
    etiquetaCorreo = Label(ventana4, text="Correo", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
     
    #Se agrega la etiqueta de contraseña
    etiquetaContrasena = Label(ventana4, text="Nueva Contraseña", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)
    
    #Se agrega la etiqueta de confirmar contraseña
    etiquetaContrasenaRe = Label(ventana4, text="Confirmar Contraseña", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)

    
    # Calcula la posición x para que la etiqueta usuario esté en el centro horizontal
    x = (ancho_pantalla - etiquetaUsuario.winfo_reqwidth()) // 2
    etiquetaUsuario.place(x=x, y=190) 
    
        # Calcula la posición x para que la etiqueta correo esté en el centro horizontal
    x = (ancho_pantalla - etiquetaCorreo.winfo_reqwidth()) // 2
    etiquetaCorreo.place(x=x, y=290) 
    
        # Calcula la posición x para que la etiqueta contraseña esté en el centro horizontal
    x = (ancho_pantalla - etiquetaContrasena.winfo_reqwidth()) // 2
    etiquetaContrasena.place(x=x, y=390) 
    
        # Calcula la posición x para que la etiqueta repetir contraseña esté en el centro horizontal
    x = (ancho_pantalla - etiquetaContrasenaRe.winfo_reqwidth()) // 2
    etiquetaContrasenaRe.place(x=x, y=490) 
    
    # Obtener el ancho de la pantalla
    ancho_pantalla = ventana4.winfo_screenwidth()

    # Calcular la posición x para centrar horizontalmente los campos de entrada
    x_entry = (ancho_pantalla) // 3.4
    
    
    # Espacio para llenar usuario
    nombreUsuario_verif2 = tk.StringVar()
    nombre_usuario2_entry = tk.Entry(ventana4, textvariable=nombreUsuario_verif2, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    nombre_usuario2_entry.place(x=x_entry, y=235)
    
    # Espacio para llenar correo
    correo_verif2 = tk.StringVar()
    correo_entry = tk.Entry(ventana4, textvariable=correo_verif2, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    correo_entry.place(x=x_entry, y=335)
    
    # Espacio para llenar contraseña
    contrasena_verif2 = tk.StringVar()
    contrasena_entry = tk.Entry(ventana4, textvariable=contrasena_verif2, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    contrasena_entry.place(x=x_entry, y=435)
    
    # Espacio para llenar contraseña repetida
    contrasenaRe_verif2 = tk.StringVar()
    contrasena_Re_entry = tk.Entry(ventana4, textvariable=contrasenaRe_verif2, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    contrasena_Re_entry.place(x=x_entry, y=535)
    
    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de registrarse de la ventana de registro
    botonRegistro = Button(ventana4, text="Guardar cambios", height="3", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command="")
    botonRegistro.place(relx=0.5, rely=0.8 + 0.03, anchor='center')
    
    # Botón de Atrás de la ventana inicio de sesión
    botonAtras = Button(ventana4, text="Atrás", height="3", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=volver_atras)
    botonAtras.place(relx=0.5, rely=0.6 + 1 * espacio_entre_botones/90, anchor='center')


    ventana4.protocol("WM_DELETE_WINDOW", volver_atras)  # Manejar cierre de ventana
    
    ventana4.mainloop()

# Función para volver atrás
def volver_atras():
    global ventana2
    if ventana2:
        ventana2.withdraw()
    if ventana1:
        ventana1.deiconify()

def insertar_datos():
    #Conexión con la base de datos local
    bd = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="bd1"
    )
    fcursor=bd.cursor()
    # Definición de la consulta SQL para INSERT
    sql = "INSERT INTO login (Correo, Usuario, Contrasena) VALUES ('{0}', '{1}', '{2}')".format(correo_usuario_entry.get(), nombre_usuario_entry.get(), contrasena_usuario_entry.get())
    
    try:
        fcursor.execute(sql)
        bd.commit()
        messagebox.showinfo(message="Has sido registrado corretamente", title="Aviso")
    except:
        bd.rollback()
        messagebox.showinfo(message="Tu registro no se pudo completar", title="Aviso")
    
    bd.close()

#Validar datos de ingreso
def validar_datos():
        #Conexión con la base de datos local
    bd = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="bd1"
    )
    fcursor = bd.cursor()
    #Verifica el inicio de sesión correcto o incorrecto.
    fcursor.execute("SELECT Contrasena FROM login WHERE usuario='"+nombreUsuario_verif.get()+"' and contrasena= '"+contrasenaUsuario_verif.get()+"'")
    if fcursor.fetchall():
        messagebox.showinfo(title="Inicio de sesión exitoso",message="Usuario y Contraseña correcta")
    
    else:
        messagebox.showinfo(title="Inicio de sesión incorrecto",message="Usuario y Contraseña incorrecta")
    bd.close()

menu_login()


def titleImage1():
    picture = pygame.image.load("welcomeInterfaceFramesSprites/savedItems/title.png")
    picture = pygame.transform.scale(picture, [550,170])
    screen.blit(picture, [386,520])

def salir():
    window.destroy()

def check_click(image_rect1, image_rect2):
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1:  # Verifica clic izquierdo
            mouse_pos = pygame.mouse.get_pos()
            if image_rect1.collidepoint(mouse_pos):
                print("Clic izquierdo en el botón!")
                abrir_login()  # Abre Login.py
            if image_rect2.collidepoint(mouse_pos):
                print("Clic")
                salir()

background = pygame.image.load('welcomeInterfaceFramesSprites/SavedItems/bg.png').convert()  
background = pygame.transform.scale(background, (screen_width, screen_height))  

# Agregar un label con el texto "battle city"
label = tk.Label(window, text="battle city", font=("Arial", 36), fg="white", bg="black")
label.place(relx=0.5, rely=0.5, anchor="center")

while True:
    for e in event.get():
        if e.type == QUIT: 
            pygame.quit()
            sys.exit()

    frame = int(time.time()*4)
    frame %= len(images)
    frame %= len(close)
    screen.blit(background, (0, 0))
    screen.blit(images[frame], (980,10))
    screen.blit(close[frame],(20,10))


    titleImage1()

    button1_rect = images[frame].get_rect(topleft=(980,10))
    button2_rect = close[frame].get_rect(topleft=(20,10))

    display.flip()

    check_click(button1_rect, button2_rect)

window.mainloop()
