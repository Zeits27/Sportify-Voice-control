import os
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state,user-modify-playback-state"
))

devices = sp.devices()
if len(devices["devices"]) == 0:
    print(" No active Spotify device found. Please open Spotify app.")
    exit()
device_id = devices["devices"][0]["id"]

recognizer = sr.Recognizer()

def record_audio(seconds=4, samplerate=16000):
    """ Rekam audio via sounddevice dan convert ke AudioData buat recognizer """
    print(" Listening...")
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    return sr.AudioData(audio.tobytes(), samplerate, 2)

while True:
    audio_data = record_audio(3)
    try:
        command = recognizer.recognize_google(audio_data).lower()
        print(f"👉 Heard: {command}")

        trigger = "spotify"
        if command.startswith(trigger):
            cmd = command.replace(trigger, "").strip()

            if "play" in cmd:
                sp.start_playback(device_id=device_id)
                print("▶Playing...")
            elif "pause" in cmd:
                sp.pause_playback(device_id=device_id)
                print("Paused.")
            elif "next" in cmd:
                sp.next_track(device_id=device_id)
                print("Next track.")
            elif "previous" in cmd or "prev" in cmd:
                sp.previous_track(device_id=device_id)
                print("Previous track.")
            elif "volume" in cmd:
                try:
                    vol = int(cmd.split("volume")[1].strip())
                    sp.volume(vol, device_id=device_id)
                    print(f"Volume set to {vol}%")
                except:
                    print("Format volume salah. Coba 'Spotify volume 30'")
            elif "stop" in cmd:
                print("Stopping voice control.")
                break
            else:
                print(" Command not recognized.")
        else:
            print(" No trigger word detected.")

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Speech recognition error:", e)
