import pyaudio
import wave
import threading
from pynput import keyboard, mouse
from transcribir import transcribir
from llm import invoke_graph


class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.output_file = "grabacion.mp3"

    def start_recording(self):
        if self.is_recording:
            print("Ya está grabando.")
            return
        self.is_recording = True
        self.frames = []
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)
        threading.Thread(target=self.record).start()
        print("Grabación iniciada...")

    def record(self):
        while self.is_recording:
            data = self.stream.read(1024, exception_on_overflow=False)
            self.frames.append(data)

    def stop_recording(self):
        if not self.is_recording:
            print("No se está grabando.")
            return
        self.is_recording = False
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.save_recording()
        print("Grabación detenida.")
        self.llm_logic()

    def save_recording(self):
        with wave.open(self.output_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))

    def llm_logic(self):
        print('Transcribiendo')
        texto = transcribir()
        print('Invocando agente')
        invoke_graph(texto)

    def cleanup(self):
        if self.audio is not None:
            self.audio.terminate()

def mouse_listener(recorder):
    def on_click(x, y, button, pressed):
        # Usa Button.xbutton1 o Button.xbutton2 para botones extras del mouse
        from pynput.mouse import Button
        if button == Button.x2:  # Botón extra izquierdo del mouse
            if pressed:
                recorder.start_recording()
            else:
                recorder.stop_recording()

    with mouse.Listener(on_click=on_click) as listener:
        print("Escuchando eventos del mouse... Presiona Ctrl+C para salir.")
        listener.join()

def keyboard_listener(recorder):
    def on_press(key):
        try:
            if key == keyboard.Key.f24:  # Detect the F24 key
                if not recorder.is_recording:
                    recorder.start_recording()
                else:
                    recorder.stop_recording()
        except Exception as e:
            print(f"Error: {e}")

    with keyboard.Listener(on_press=on_press) as listener:
        print("Escuchando eventos del teclado... Usa F24 para iniciar/detener la grabación. Presiona Ctrl+C para salir.")
        listener.join()


if __name__ == "__main__":
    recorder = AudioRecorder()

    try:
        mouse_listener(recorder)
        #keyboard_listener(recorder)
    except KeyboardInterrupt:
        print("\nSaliendo...")
        recorder.cleanup()
