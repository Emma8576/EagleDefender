import tkinter as tk
import json

def abrir_ventana_configuracion():
    ventana_configuracion = tk.Toplevel(root)

    def cambiar_idioma_configuracion():
        idioma_seleccionado = var_idioma.get()
        texto_traducido = traducciones[texto_original][idioma_seleccionado]
        label.config(text=texto_traducido)
        guardar_configuracion(idioma_seleccionado)
        ventana_configuracion.destroy()

    var_idioma = tk.StringVar(ventana_configuracion)

    menu_idioma = tk.OptionMenu(ventana_configuracion, var_idioma, * opciones_idioma)
    menu_idioma.pack()

    boton_cambiar_idioma = tk.Button(ventana_configuracion, text="Cambiar Idioma", command=cambiar_idioma_configuracion)
    boton_cambiar_idioma.pack()

    # Configurar ventana de configuración para que ocupe toda la pantalla
    ventana_configuracion.wm_attributes('-fullscreen', '1')


def cambiar_idioma():
    idioma_seleccionado = var_idioma.get()
    texto_traducido = traducciones[texto_original][idioma_seleccionado]
    label.config(text=texto_traducido)
    guardar_configuracion(idioma_seleccionado)

def guardar_configuracion(idioma):
    with open('configuracion.json', 'w') as archivo:
        json.dump({'idioma': idioma}, archivo)

def cargar_configuracion():
    try:
        with open('configuracion.json', 'r') as archivo:
            configuracion = json.load(archivo)
            return configuracion['idioma']
    except FileNotFoundError:
        return None

# Crear la ventana principal
root = tk.Tk()
root.attributes("-fullscreen", True)

# Crear una variable que almacenará el idioma seleccionado
var_idioma = tk.StringVar(root)

# Crear una lista de opciones de idiomas
opciones_idioma = ["Español", "Inglés", "Francés", "Furra"]

# Intentar cargar la última configuración del usuario
idioma_guardado = cargar_configuracion()

# Establecer el idioma predeterminado (o el último seleccionado por el usuario)
var_idioma.set(idioma_guardado if idioma_guardado in opciones_idioma else opciones_idioma[0])

# Crear un botón para abrir la ventana de configuración
boton_configuracion = tk.Button(root, text="Configuración", command=abrir_ventana_configuracion)
boton_configuracion.pack()

# Crear un diccionario de traducciones
traducciones = {
    "Saludo": {
        "Español": "¡Hola!",
        "Inglés": "Hello!",
        "Francés": "Bonjour!",
        "Furra": "Vos"
    }
}

# Texto original del label
texto_original = "Saludo"

# Crear un label con el texto original
label = tk.Label(root, text=traducciones[texto_original][var_idioma.get()])
label.pack()

# Iniciar el bucle principal de la aplicación
root.mainloop()
