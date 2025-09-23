import os
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from spotify_utils import ensure_track_in_current_playlist

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state user-modify-playback-state playlist-read-private playlist-modify-private playlist-modify-public",
    open_browser=False,
    cache_path=os.path.join(os.getcwd(), ".cache")
))


devices = sp.devices()
if len(devices["devices"]) == 0:
    print(" No active Spotify device found. Please open Spotify app.")
    exit()
device_id = devices["devices"][0]["id"]

recognizer = sr.Recognizer()

def record_audio(seconds=4, samplerate=16000):
    print(" Listening...")
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    return sr.AudioData(audio.tobytes(), samplerate, 2)

listening_mode = False  

while True:
    audio_data = record_audio(3)
    try:
        command = recognizer.recognize_google(audio_data).lower()
        print(f"👉 Heard: {command}")

        if not listening_mode:
           
            if "spotify" in command:
                listening_mode = True
                print("🎤 Spotify mode ON. Say a command...")
            else:
                print(" No trigger word detected.")
        else:
           
            if "play" in command:
                sp.start_playback(device_id=device_id)
                print("▶Playing...")
            elif "pause" in command:
                sp.pause_playback(device_id=device_id)
                print("Paused.")
            elif "next" in command:
                sp.next_track(device_id=device_id)
                print("Next track.")
            elif "previous" in command or "prev" in command:
                sp.previous_track(device_id=device_id)
                print("Previous track.")
            elif "volume" in command:
                try:
                    vol = int(command.split("volume")[1].strip())
                    sp.volume(vol, device_id=device_id)
                    print(f"Volume set to {vol}%")
                except:
                    print("Format volume salah. Coba 'Spotify volume 30'")
            elif "add" in command:
                playlist_id, track_id, added = ensure_track_in_current_playlist(sp)
                if playlist_id:
                    if added:
                        print(f"Track {track_id} added to playlist {playlist_id}.")
                    else:
                        print(f"Track {track_id} already exists in playlist {playlist_id}.")
            elif "stop" in command:
                print("Stopping voice control.")
                break
            elif "exit spotify" in command:
                listening_mode = False
                print("❌ Spotify mode OFF. Say 'spotify' again to re-activate.")
            else:
                print(" Command not recognized.")

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Speech recognition error:", e)
