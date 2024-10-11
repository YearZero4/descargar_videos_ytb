from flask import Flask, render_template, request, send_file, abort
import yt_dlp
import os

app = Flask(__name__)

def descargar_video(link, output_path='video.mp4'):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['input_text']
        if descargar_video(user_input):
            return send_file('video.mp4', as_attachment=True)
        else:
            return "Error al descargar el video. Por favor revisa el enlace y vuelve a intentarlo.", 400
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))

