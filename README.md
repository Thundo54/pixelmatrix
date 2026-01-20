# 🎵 Pixel Matrix

A Python-based project that connects **Spotify** with a **32x32 LED pixel matrix**, displaying the currently playing track or podcast cover art in real time. The script uses **Spotipy** for Spotify integration and **pypixelcolor** over **WebSocket** to control the LED panel.

---

## ✨ Features

* 🎧 Real-time monitoring of Spotify playback (tracks & podcasts)
* 🖼️ Automatic download of album or podcast cover art
* 🔲 High-quality image resizing to 32x32 pixels (Pillow / LANCZOS)
* 🌐 WebSocket communication with a pypixelcolor LED server
* 🔄 Automatic update when the track changes
* ⏸️ Fallback image when playback is stopped
* 🔐 Secure configuration using `.env` environment variables

---

## 🧰 Tech Stack

* **Python 3.9+**
* **Spotify Web API** (Spotipy)
* **Pillow** – image processing
* **WebSocket Client** – LED communication
* **pypixelcolor** – LED matrix control
* **python-dotenv** – environment configuration

---

## ⚙️ Requirements

### Hardware

* 32x32 LED matrix compatible with pypixelcolor
* Running pypixelcolor WebSocket server

### Software

* Spotify Developer account
* Python environment with required dependencies

Install dependencies:

```bash
pip install spotipy requests pillow websocket-client python-dotenv
```

---

## 🔑 Configuration

Create a `.env` file in the project directory:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=spotify_redirect_uri
PYPIXEL_WS_URL=pypixelcolor_websocket_url
```

Make sure the redirect URI is set correctly in the Spotify Developer Dashboard.

---

## ▶️ Usage

Start the script with:

```bash
python spotify_pixel_matrix.py
```

On first run, your browser will open to authorize access to your Spotify account.

---

## 🖼️ Assets

Place the following images in the project directory:

* `pixelmatrix.png` – shown when WebSocket connects
* `playback_stop.png` – shown when playback is stopped

The current cover art is downloaded and saved dynamically as:

```
cover.png
```

---

## 🧠 How It Works

1. Connects to Spotify using OAuth
2. Continuously checks the current playback state
3. Detects track or podcast changes
4. Downloads and resizes cover art
5. Sends the image path to the LED matrix via WebSocket

---

## 🚀 Future Ideas

* Text scrolling with track title and artist
* Smooth transitions and animations
* Support for larger LED matrices
* Multi-service support (e.g. YouTube Music)

---

## 📜 License

MIT

---

Made with ❤️ by **Thundo**
