from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from PIL import Image
import spotipy
import requests
import time
import json
import websocket
import threading
import io
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
PYPIXEL_WS_URL = os.getenv('PYPIXEL_WS_URL')

SPOTIFY_SCOPE = 'user-read-currently-playing user-read-playback-state'

def on_close(ws, close_status_code, close_msg):
    print(f'Rozłączono z WebSocket ({PYPIXEL_WS_URL})')

def on_open(ws):
    print(f'Połączono z WebSocket ({PYPIXEL_WS_URL})')
    update_led_panel('assets/pixelmatrix.png')

def on_reconnect(ws):
    print(f'Przywrócono połączenie z WebSocket ({PYPIXEL_WS_URL})')
    update_led_panel('cover.png')

def send_ws_command(command, params_list):
    try:
        if pixelcolor_websocket.sock and pixelcolor_websocket.sock.connected:
            payload = {'command': command, 'params': params_list}
            pixelcolor_websocket.send_text(json.dumps(payload))
            return True
        else:
            print('WebSocket nie jest jeszcze połączony...')
            return False
    except Exception as e:
        print(f'Błąd wysyłania komendy WebSocket: {e}')
        return False


def connect_to_websocket():
    print(f'Łączenie z WebSocket ({PYPIXEL_WS_URL})...')
    pixelcolor_websocket.run_forever(reconnect=5)

def update_led_panel(path):
    img_params = [f'path={path}']
    return send_ws_command('send_image', img_params)

def download_cover(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            image_buffer = io.BytesIO(resp.content)
            img = Image.open(image_buffer)
            img_resized = img.resize((32, 32), Image.Resampling.LANCZOS)
            img_resized.save('cover.png')
            return update_led_panel('cover.png')
    except Exception as e:
        print(f'Błąd pobierania okładki: {e}')
    return False


def main_spotify_loop():
    last_item_id = None
    print('Wątek Spotify uruchomiony. Monitorowanie...')

    while True:
        try:
            current_track = spotify_api.current_user_playing_track(additional_types=['episode'])

            if current_track and current_track.get('is_playing'):
                item = current_track.get('item')
                if not item:
                    continue

                item_id = item.get('id')

                if item_id != last_item_id:
                    track_name = item.get('name')
                    playing_type = current_track.get('currently_playing_type')

                    if playing_type == 'track':
                        artist_or_show = item['artists'][0]['name']
                        cover_url = item['album']['images'][0]['url']
                    elif playing_type == 'episode':
                        artist_or_show = item['show']['name']
                        cover_url = item['show']['images'][0]['url'] if item['show'].get('images') else item['images'][0]['url']
                    else:
                        artist_or_show, cover_url = 'Spotify', None

                    print(f'Teraz odtwarzane: {artist_or_show} - {track_name}')

                    if cover_url:
                        if download_cover(cover_url):
                            last_item_id = item_id
            else:
                if last_item_id is not None:
                    print('Odtwarzanie zatrzymane.')
                    update_led_panel('assets/playback_stop.png')
                    last_item_id = None

        except Exception as e:
            print(f'Błąd API Spotify: {e}')
            time.sleep(2)

        time.sleep(1)


if __name__ == '__main__':
    try:
        pixelcolor_websocket = websocket.WebSocketApp(PYPIXEL_WS_URL, on_open=on_open, on_close=on_close, on_reconnect=on_reconnect)
        spotify_api = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=SPOTIFY_REDIRECT_URI, scope=SPOTIFY_SCOPE))
        spotify_thread = threading.Thread(target=main_spotify_loop, daemon=True).start()
        connect_to_websocket()
    except KeyboardInterrupt:
        print('\nZamykanie skryptu...')