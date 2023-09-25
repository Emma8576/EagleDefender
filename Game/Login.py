import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pymysql

# Variables globales para las ventanas
ventana1 = None
ventana2 = None

#Se agrega imagen de fondo
def cargar_imagen_de_fondo(ventana, ruta_imagen):
    # Cargar la imagen de fondo
    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)

    # Crear una etiqueta para mostrar la imagen de fondo
    etiqueta_fondo = Label(ventana, image=imagen)
    etiqueta_fondo.image = imagen  # Mantener una referencia a la imagen
    etiqueta_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Cubrir toda la ventana

#Función ventana Login
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

    # Mostrar la ventana principal
    ventana1.mainloop()

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
    fuente_retro_1 = ("8-Bit Operator+ 8", 50)
    fuente_retro_2 = ("8-Bit Operator+ 8", 25)
    fuente_retro_3 = ("8-Bit Operator+ 8", 15)
    
    #Etiqueta con el nombre del juego
    etiqueta_retro = Label(ventana4, text="Battle City", bg="#000030", font=fuente_retro, fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5, anchor='center') 
    etiqueta_retro.pack()
    
    #Etiqueta de registro del juego
    ancho_pantalla = ventana4.winfo_screenwidth()
    etiqueta = Label(ventana4, text="Recuperar acceso", bg="#101654", fg="white", font=fuente_retro_1)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=120)
    
    #variables para almacenar los datos ingresados por el usuario
    nombreUsuarioOCorreo_verif = StringVar() 

    #Se agrega la etiqueta de usuario
    etiquetaUsuarioOCorreo = Label(ventana4, text="Ingresa tu Correo o Usuario", bg="#1b0945", height="1", relief="ridge", fg="white", borderwidth=5, font=fuente_retro_2)  
     
    # Calcula la posición x para que la etiqueta usuario esté en el centro horizontal
    x = (ancho_pantalla - etiquetaUsuarioOCorreo.winfo_reqwidth()) // 2
    etiquetaUsuarioOCorreo.place(x=x, y=220) 
    
    # Obtener el ancho de la pantalla
    ancho_pantalla = ventana4.winfo_screenwidth()

    # Calcular la posición x para centrar horizontalmente los campos de entrada
    x_entry = (ancho_pantalla) // 3.4
    
    
    # Espacio para llenar usuario
    nombreUsuarioOCorreo_verif = tk.StringVar()
    nombre_usuarioOC_entry = tk.Entry(ventana4, textvariable=nombreUsuarioOCorreo_verif, bg="#9e2254", fg="white", font=fuente_retro_2, relief="groove", borderwidth=10, width=23)
    nombre_usuarioOC_entry.place(x=x_entry, y=280)
    
    # Espacio entre botones
    espacio_entre_botones = 30 

    # Botón de registrarse de la ventana de registro
    botonRegistro = Button(ventana4, text="Enviar correo", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command="")
    botonRegistro.place(relx=0.5, rely=0.5, anchor='center')
    
    # Botón de Atrás de la ventana inicio de sesión
    botonAtras = Button(ventana4, text="Atrás", height="4", width="30", background="#0a0c3f", fg="white", font=fuente_retro_3, relief="raised", borderwidth=10, command=volver_atras)
    botonAtras.place(relx=0.5, rely=0.3 + 1 * espacio_entre_botones/90, anchor='center')


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
