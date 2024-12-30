from openai import OpenAI

client = OpenAI()

def transcribir():
    audio_file= open('grabacion.mp3', "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text

