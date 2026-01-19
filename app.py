from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_link', methods=['POST'])
def get_link():
    url = request.form.get('video_url')
    if not url:
        return render_template('index.html', error="Kripya URL paste karein!")

    try:
        # User-Agent add kiya gaya hai taaki YouTube block na kare
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title')
            thumb = info.get('thumbnail')

        return render_template('index.html', 
                             direct_url=video_url, 
                             title=title, 
                             thumb=thumb)

    except Exception as e:
        # Asli error check karne ke liye console log
        print(f"Error: {e}")
        return render_template('index.html', error="YouTube ne security block laga diya hai. Dusra video link try karein ya 5 min baad koshish karein.")

app = app
