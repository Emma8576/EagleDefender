import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pygame
from PIL import Image, ImageTk
import subprocess
import sys
import time
import pymysql
from tkinter import simpledialog

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
fuente = ("Arial", 12)


# Se agrega imagen de fondo
def cargar_imagen_de_fondo(ventana_1, ruta_imagen):
    # Cargar la imagen de fondo
    imagen = Image.open(ruta_imagen)
    imagen = ImageTk.PhotoImage(imagen)
    return imagen


def volver_inicio_sesion():
    archivo = 'Login.py'
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
    archivo_partida = 'panel.py'

    # obtener los nombres de usuario y roles seleccionados
    usuario_defensor = etiqueta_jugador_1.cget("text").split(": ")[1]
    usuario_atacante = etiqueta_jugador_2.cget("text").split(": ")[1]
    
    # Guardar los roles en el archivo de texto
    with open('nombres_usuarios.txt', 'w') as file:
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
    etiqueta_retro = Label(ventana_1,
                           text="Battle City",
                           bg="#000030",
                           font=fuente_retro_6,
                           fg="white")
    etiqueta_retro.place(relx=0.5, rely=0.5, anchor='center')
    etiqueta_retro.pack()


    # Función para mostrar el menú de los roles en la posición del botón
    def mostrar_menu_3(event):
        menu_principal_3.delete(0, "end")
        usuarios = cargar_nombres_usuarios()
        for usuario in usuarios:
            menu_principal_3.add_command(label=usuario,
                                         font=fuente_retro_9,
                                         foreground="white",
                                         background="#101654",
                                         command=lambda u=usuario: seleccionar_defensor(u))
        menu_principal_3.post(event.x_root, event.y_root)

    def seleccionar_defensor(usuario):
        etiqueta_jugador_1.config(text=f"Defensor: {usuario}")
        otros_usuarios = [u for u in cargar_nombres_usuarios() if u != usuario]
        if otros_usuarios:
            seleccionar_atacante(otros_usuarios[0])
        # Imprimir el usuario en la terminal
        print(f"El usuario defensor es: {usuario}")

    # Función para obtener los nombres de usuario de los roles
    def obtener_nombres_roles():
        try:
            with open('nombres_usuarios.txt', 'r') as file:
                lineas = file.readlines()
                usuario_defensor = lineas[0].strip().split(": ")[1]
                usuario_atacante = lineas[1].strip().split(": ")[1]
                return usuario_defensor, usuario_atacante
        except FileNotFoundError:
            print("El archivo nombres_usuarios.txt no fue encontrado.")

    # Ejemplo de uso
    nombre_defensor, nombre_atacante = obtener_nombres_roles()
    print(f"El defensor es: {nombre_defensor}")
    print(f"El atacante es: {nombre_atacante}")

    
 ###########################iNICIO BASE DE DATOS##################################################################   
 
    def guardar_cancion_en_db(nombre_cancion, archivo_cancion, popularidad, bailabilidad):
        try:
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="bd1",
                charset="utf8",
                connect_timeout=60
            )

            with open(archivo_cancion, 'rb') as archivo_mp3:
                contenido_mp3 = archivo_mp3.read()

                with conexion.cursor() as cursor:
                    # Sentencia SQL para insertar la canción en la tabla canciones
                    sql = "INSERT INTO canciones (nombre_cancion, archivo_cancion, popularidad, bailabilidad) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (nombre_cancion,
                                         contenido_mp3,
                                         popularidad,
                                         bailabilidad))

                conexion.commit()
                print("Canción agregada correctamente a la base de datos.")

        except pymysql.Error as e:
            print(f"Error al insertar la canción en la base de datos: {str(e)}")
        finally:
            if conexion:
                conexion.close()


    def abrir_ventana_seleccion(nombre_usuario):
        canciones = filedialog.askopenfilenames(initialdir="/",
                                                title=f"Elegir música de {nombre_usuario}",
                                                filetypes=(("Archivos MP3",
                                                            "*.mp3"),
                                                           ("Todos los archivos",
                                                            "*.*")))
        # Obtener la ventana raíz actual o la ventana principal
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana raíz
        
        for cancion in canciones:
            nombre_cancion = cancion.split("/")[-1]
            
            # Pedir al usuario la popularidad de la canción en una escala de 0 a 100
            popularidad = simpledialog.askinteger("Popularidad",
                                                  f"Ingrese la popularidad de '{nombre_cancion}' (0-100):",
                                                  minvalue=0,
                                                  maxvalue=100,
                                                  parent=root)
            if popularidad is None:
                # Si el usuario cancela la entrada, continuar con la siguiente canción
                continue
                
            # Pedir al usuario la bailabilidad de la canción en una escala de 0 a 100
            bailabilidad = simpledialog.askinteger("Bailabilidad",
                                                   f"Ingrese la bailabilidad de '{nombre_cancion}' (0-100):",
                                                   minvalue=0,
                                                   maxvalue=100,
                                                   parent=root)
            if bailabilidad is None:
                # Si el usuario cancela la entrada, continuar con la siguiente canción
                continue
                
            guardar_cancion_en_db(nombre_cancion, cancion, popularidad, bailabilidad)
            asociar_usuario_cancion(nombre_usuario, nombre_cancion)
            actualizar_canciones_defensor()
            actualizar_canciones_atacante()
            print(f"Canción '{nombre_cancion}' guardada en la base de datos con popularidad: {popularidad}, bailabilidad: {bailabilidad}")

        root.destroy()  # Cerrar la ventana raíz después de completar el proceso

    nombre_defensor, nombre_atacante = obtener_nombres_roles()
    def obtener_id_usuario_por_nombre(nombre_usuario):
        try:
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="bd1",
                charset="utf8",
                connect_timeout=60
            )

            with conexion.cursor() as cursor:
                # Consulta SQL para obtener el id del usuario por su nombre
                sql = "SELECT ID FROM login WHERE Usuario = %s"
                cursor.execute(sql, (nombre_usuario,))
                result = cursor.fetchone()

                if result:
                    return result[0]  
                else:
                    return None 
        except pymysql.Error as e:
            print(f"Error al obtener el id del usuario por su nombre: {str(e)}")
        finally:
            if conexion:
                conexion.close()
                
    
    def obtener_id_cancion_por_nombre(nombre_cancion):
        try:
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="bd1",
                charset="utf8",
                connect_timeout=60
            )

            with conexion.cursor() as cursor:
                # Consulta SQL para obtener el id de la canción por su nombre
                sql = "SELECT ID FROM canciones WHERE nombre_cancion = %s"
                cursor.execute(sql, (nombre_cancion,))
                result = cursor.fetchone()

                if result:
                    return result[0]  # Devuelve el id de la canción
                else:
                    return None  # Si no se encuentra la canción
        except pymysql.Error as e:
            print(f"Error al obtener el id de la canción por su nombre: {str(e)}")
        finally:
            if conexion:
                conexion.close() 
                
    
    def guardar_seleccion_usuario_cancion(id_usuario, id_cancion):
        try:
            # Conectar a la base de datos
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="bd1", 
                charset="utf8",
                connect_timeout=60
            )

            with conexion.cursor() as cursor:
                # Sentencia SQL para insertar la selección de usuario y canción en la tabla usuarios_canciones
                sql = "INSERT INTO usuarios_canciones (id_usuario, id_cancion) VALUES (%s, %s)"
                cursor.execute(sql, (id_usuario, id_cancion))

            # Confirmar la operación de inserción y cerrar la conexión
            conexion.commit()
            print("Selección de canción asociada al usuario guardada correctamente en la base de datos.")

        except pymysql.Error as e:
            print(f"Error al insertar la selección de canción asociada al usuario en la base de datos: {str(e)}")
        finally:
            if conexion:
                conexion.close()

    # Funciones para obtener el ID del usuario y el ID de la canción
    nombre_defensor, nombre_atacante = obtener_nombres_roles()
    id_defensor = obtener_id_usuario_por_nombre(nombre_defensor)
    id_atacante = obtener_id_usuario_por_nombre(nombre_atacante)

    def asociar_usuario_cancion(nombre_usuario, nombre_cancion):
        # Obtener el ID del usuario y de la canción
        id_usuario = obtener_id_usuario_por_nombre(nombre_usuario)
        id_cancion = obtener_id_cancion_por_nombre(nombre_cancion)

        if id_usuario and id_cancion:
            # Guardar la selección de usuario y canción en la base de datos
            guardar_seleccion_usuario_cancion(id_usuario, id_cancion)
        else:
            print("El usuario o la canción no se encontraron en la base de datos.")


    def obtener_canciones_defensor(nombre_usuario_defensor):
        canciones_defensor = []
        try:
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="bd1",
                charset="utf8",
                connect_timeout=60
            )

            with conexion.cursor() as cursor:
                # Consulta SQL para obtener el ID del usuario defensor por su nombre
                sql_usuario = "SELECT ID FROM login WHERE Usuario = %s"
                cursor.execute(sql_usuario, (nombre_usuario_defensor,))
                id_usuario_defensor = cursor.fetchone()

                if id_usuario_defensor:
                    # Consulta SQL para obtener las canciones asociadas al ID del usuario defensor
                    sql_canciones = """
                        SELECT c.nombre_cancion 
                        FROM usuarios_canciones uc
                        JOIN canciones c ON uc.id_cancion = c.ID
                        WHERE uc.id_usuario = %s
                    """
                    cursor.execute(sql_canciones, (id_usuario_defensor[0],))
                    result = cursor.fetchall()

                    if result:
                        canciones_defensor = [cancion[0] for cancion in result]

        except pymysql.Error as e:
            print(f"Error al obtener las canciones asociadas al usuario defensor por nombre: {str(e)}")
        finally:
            if conexion:
                conexion.close()

        return canciones_defensor

    def actualizar_canciones_defensor():
        # Obtener las canciones asociadas al usuario defensor actual por su nombre
        canciones_defensor_actual = obtener_canciones_defensor(nombre_defensor)

        # conjunto (set) para almacenar canciones únicas
        canciones_unicas = set(canciones_defensor_actual)

        # Crear la Listbox y agregar las canciones únicas
        listbox_canciones_defensor = tk.Listbox(ventana_1,
                                                width=40,
                                                height=8,
                                                bg="navy",
                                                fg="white")
        listbox_canciones_defensor.place(relx=0.40, rely=0.5 - 0.06)

        listbox_canciones_defensor.configure(font=fuente)

        # Insertar las canciones únicas en la Listbox
        for cancion in canciones_unicas:
            listbox_canciones_defensor.insert(tk.END, cancion)
    # Llamar a la función para actualizar las canciones por primera vez
    actualizar_canciones_defensor()

    def obtener_canciones_atacante(nombre_usuario_atacante):
        canciones_atacante = []
        try:
            conexion = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="bd1",
                charset="utf8",
                connect_timeout=60
            )

            with conexion.cursor() as cursor:
                # Consulta SQL para obtener el ID del usuario defensor por su nombre
                sql_usuario = "SELECT ID FROM login WHERE Usuario = %s"
                cursor.execute(sql_usuario, (nombre_usuario_atacante,))
                id_usuario_atacante = cursor.fetchone()

                if id_usuario_atacante:
                    # Consulta SQL para obtener las canciones asociadas al ID del usuario defensor
                    sql_canciones = """
                        SELECT c.nombre_cancion 
                        FROM usuarios_canciones uc
                        JOIN canciones c ON uc.id_cancion = c.ID
                        WHERE uc.id_usuario = %s
                    """
                    cursor.execute(sql_canciones, (id_usuario_atacante[0],))
                    result = cursor.fetchall()

                    if result:
                        canciones_atacante = [cancion[0] for cancion in result]

        except pymysql.Error as e:
            print(f"Error al obtener las canciones asociadas al usuario atacante por nombre: {str(e)}")
        finally:
            if conexion:
                conexion.close()

        return canciones_atacante

    def actualizar_canciones_atacante():
        # Obtener las canciones asociadas al usuario atacante actual por su nombre
        canciones_atacante_actual = obtener_canciones_atacante(nombre_atacante)

        # conjunto para almacenar canciones únicas
        canciones_unicas = set(canciones_atacante_actual)

        # Crear la Listbox y agregar las canciones únicas
        listbox_canciones_defensor = tk.Listbox(ventana_1,
                                                width=40,
                                                height=8,
                                                bg="navy",
                                                fg="white")
        listbox_canciones_defensor.place(relx=0.40, rely=0.5 + 0.25)

        listbox_canciones_defensor.configure(font=fuente)

        # Insertar las canciones únicas en la Listbox
        for cancion in canciones_unicas:
            listbox_canciones_defensor.insert(tk.END, cancion)
    # Llamar a la función para actualizar las canciones por primera vez
    actualizar_canciones_atacante()

    ###########################FIN BASE DE DATOS##################################################################

    # Crear botón y asociar con abrir_ventana_seleccion usando el nombre del defensor
    boton_menu = tk.Button(ventana_1,
                           text=f"Elegir música de {nombre_defensor}",
                           font=fuente_retro_5,
                           bg="#101654",
                           fg="white",
                           activebackground="blue",
                           relief="groove",
                           border=5,
                           width=25,
                           height=3,
                           command=lambda: abrir_ventana_seleccion(nombre_defensor))
    boton_menu.place(relx=0.4, rely=0.5 - 0.16)

    # Crear botón y asociar con abrir_ventana_seleccion usando el nombre del atacante
    boton_menu_2 = tk.Button(ventana_1,
                             text=f"Elegir música de {nombre_atacante}",
                             font=fuente_retro_5,
                             bg="#101654",
                             fg="white",
                             activebackground="blue",
                             relief="groove",
                             border=5,
                             width=25,
                             height=3,
                             command=lambda: abrir_ventana_seleccion(nombre_atacante))
    boton_menu_2.place(relx=0.4, rely=0.6 + 0.06)

    # Crear el botón y menú desplegable de los roles
    boton_menu_3 = tk.Button(ventana_1,
                             text="Usuarios ⬇",
                             font=fuente_retro_5,
                             bg="#101654",
                             fg="white",
                             activebackground="blue",
                             width=20,
                             height=3,
                             relief="groove",
                             border=5)
    boton_menu_3.place(relx=0.5 - 0.09, rely=0.3 - 0.05)

    menu_principal_3 = Menu(ventana_1, tearoff=0)

    boton_menu_3.bind("<Button-1>", mostrar_menu_3)

    # Etiqueta de Configurar partida
    ancho_pantalla = ventana_1.winfo_screenwidth()
    global etiqueta
    etiqueta = Label(ventana_1,
                     text="Configurar partida",
                     bg="#101654",
                     fg="white",
                     font=fuente_retro_8)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla - etiqueta.winfo_reqwidth()) // 2
    etiqueta.place(x=x, y=100)

    # Etiqueta de jugador 1
    ancho_pantalla_1 = ventana_1.winfo_screenwidth()
    global etiqueta_jugador_1
    etiqueta_jugador_1 = Label(ventana_1,
                               text="Defensor: ¿?",
                               bg="#101654",
                               fg="white",
                               font=fuente_retro_3,
                               height=2,
                               width=20)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    #x = (ancho_pantalla_1 - etiqueta.winfo_reqwidth()) * 1
    etiqueta_jugador_1.place(relx= 0.1 - 0.05, rely=0.2 + 0.05)

    # Etiqueta de jugador 2
    ancho_pantalla_2 = ventana_1.winfo_screenwidth()
    global etiqueta_jugador_2
    etiqueta_jugador_2 = Label(ventana_1,
                               text="Atacante: ¿?",
                               bg="#101654",
                               fg="white",
                               font=fuente_retro_3,
                               height=2, width=20)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla_2 - etiqueta.winfo_reqwidth()) * 1
    etiqueta_jugador_2.place(relx=0.65, rely=0.2 + 0.05)

    # Etiqueta de jugador rol
    ancho_pantalla_1 = ventana_1.winfo_screenwidth()
    etiqueta_roles = Label(ventana_1,
                           text="Elige el usuario defensor",
                           bg="#101654",
                           fg="white",
                           font=fuente_retro_4)

    # Calcula la posición x para que la etiqueta esté en el centro horizontal
    x = (ancho_pantalla_1 - etiqueta.winfo_reqwidth()) // 4
    etiqueta_roles.place(relx=0.5 - 0.15, rely=0.5 - 0.3)

    # Botón de Iniciar Partida
    global boton_inicio
    boton_inicio = tk.Button(ventana_1, cursor="exchange",
                             text="Iniciar partida",
                             height="4", width="20",
                             background="#0a0c3f",
                             fg="white",
                             font=fuente_retro_5,
                             relief="raised",
                             borderwidth=10,
                             command=iniciar_partida)
    boton_inicio.place(relx=0.5 + 0.35, rely=0.5 + 0.40, anchor='center')

    # Espacio entre botones
    espacio_entre_botones = 30

    # Botón de Salir
    global boton_salir
    boton_salir = tk.Button(ventana_1,
                            cursor="exchange",
                            text="Regresar",
                            height="4",
                            width="20",
                            background="#0a0c3f",
                            fg="white",
                            font=fuente_retro_5,
                            relief="raised",
                            borderwidth=10,
                            command=volver_inicio_sesion)
    boton_salir.place(relx=0.5 - 0.35, rely=0.5 + 0.40, anchor='center')

    # Mostrar la ventana principal
    ventana_1.mainloop()


configurar_partida()
