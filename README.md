# 🎵 Spotify Voice Control

Voice assistant sederhana buat **kontrol Spotify** (play, pause, next, prev, volume) dengan **perintah suara**.  
Dibuat pakai [Spotipy](https://spotipy.readthedocs.io/) + [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) + [sounddevice](https://python-sounddevice.readthedocs.io/).

---

## Fitur

- Kendali Spotify via suara
- **Play/Pause**
- **Next track / Previous track**
- **Atur volume (0–100)**
- **Stop loop**

---

## Setup

1. **Clone repo** & masuk folder

   ```bash
   git clone https://github.com/Zeits27/Sportify-Voice-control.git
   cd spotify-voice
   ```

2. **Buat virtual environment** (opsional tapi disarankan)

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Atau manual:

   ```bash
   pip install sounddevice soundfile SpeechRecognition spotipy python-dotenv
   ```

4. **Buat file `.env`** di root project

   ```env
   SPOTIPY_CLIENT_ID=isi_client_id_lo
   SPOTIPY_CLIENT_SECRET=isi_client_secret_lo
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback/
   ```

   👉 Client ID & Secret bisa lo dapet dari [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

5. **Jalankan program**
   ```bash
   python main.py
   ```

---

## 🎤 Contoh Voice Command

- `Spotify play`
- `Spotify pause`
- `Spotify next`
- `Spotify previous`
- `Spotify volume 40`
- `Spotify stop`

---

## Catatan

- Harus punya **Spotify Premium** biar bisa kontrol playback.
- Pastikan **Spotify app** terbuka dan aktif di device lo.
- Hanya jalan di device yang sedang aktif di akun Spotify lo.
