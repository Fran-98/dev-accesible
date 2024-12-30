# tools hacen algo y devuelven un valor str para que el modelo sepa que se ejecutó
from pynput.keyboard import Controller
import pyperclip

def escribir(texto: str):
    """funcion que escribe lo que el usuario quiere escribir"""
    keyboard = Controller()
    
    for char in texto:
        keyboard.type(char)  # Simulate typing the character
        # time.sleep(0.001)  # Add delay between keystrokes

def ver_texto_copiado():
    """funcion que devuelve el texto copiado en el clipboard"""
    print(pyperclip.paste())
    return pyperclip.paste()


tools = [escribir, ver_texto_copiado]