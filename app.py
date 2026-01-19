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
        # download=False taaki aapka server load na le
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'nocheckcertificate': True
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

    except Exception:
        return render_template('index.html', error="Video link nahi mil paya. Dusra link try karein.")

# Vercel requirements
app = app
