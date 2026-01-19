from flask import Flask, render_template, request
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_link', methods=['POST'])
def get_link():
    url = request.form.get('video_url')
    if not url:
        return render_template('index.html', error="Kripya URL paste karein!")

    # Cookies file ka rasta (path)
    cookie_path = 'cookies.txt'

    try:
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True,
            # Ye line block ko bypass karegi
            'cookiefile': cookie_path if os.path.exists(cookie_path) else None,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return render_template('index.html', 
                                 direct_url=info.get('url'), 
                                 title=info.get('title'), 
                                 thumb=info.get('thumbnail'))

    except Exception as e:
        print(f"Error detail: {e}")
        return render_template('index.html', error="Cookies update karne ki zaroorat hai ya YouTube ne block kiya hai.")

app = app
