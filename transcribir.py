from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def transcribir():
    with open('grabacion.mp3', "rb") as file:
        transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=file
        )
        return transcription.text

