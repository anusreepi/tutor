from flask import Flask, render_template, request,send_from_directory
from gtts import gTTS
import os
import wav2lip
import subprocess
# Initialize ChatterBot chatbot


# Initialize Flask app
app = Flask(__name__)

# Define routes
@app.route('/')
def home():
    return render_template('index.html')

def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    # Open the file in binary write mode and use 'wb'
    with open(filename, 'wb') as f:
        # Write the audio data to the file object
        tts.write_to_fp(f)

@app.route('/chatbot_response', methods=['POST'])
def chatbot_response():
    # Get user input from the form
    user_input = request.form['user_input']
    # Perform lip-syncing with Wav2Lip
    if user_input=="hi":
        response="hi, how can I help you"
    elif user_input=="hello":
        response="hello,how are you doing today."
    else:
        response="hello,I am your bot for the dat."
    tts = gTTS(text=response, lang='en')
    tts_path = 'talking_audio.mp3'
    tts.save(tts_path)
    audio_path="/Users/anupromod/Desktop/tutor/talking_audio.mp3"
    video_path = '/Users/anupromod/Desktop/tutor/talking_video.mp4'
    video_path= generate_talking_video(audio_path, video_path)
    

    # Display lip-synced video in the frontend
    return render_template('index.html', video_url=video_path)
def generate_talking_video(audio_path, video_path):
    # Change directory to the wav2lip directory
    os.chdir('/Users/anupromod/Desktop/tutor/wav2lip')

    # Run the lip-syncing command
    subprocess.run(f'python inference.py --checkpoint_path /Users/anupromod/Desktop/wavsync/wav2lip/checkpoints/wav2lip_gan.pth --face "/Users/anupromod/Desktop/tutor/kim_7s_raw.mp4" --audio {audio_path} --outfile {video_path}', shell=True)

    # Change back to the original directory
    os.chdir('..')
    return video_path

@app.route('/Users/anupromod/Desktop/tutor/talking_video.mp4',methods=['GET'])
def serve_video():
    return send_from_directory('/Users/anupromod/Desktop/tutor/', 'talking_video.mp4')
# Run the Flask app
if __name__ == '__main__':
    app.run()
