from flask import (Flask, make_response,flash,request,redirect,
                    send_file,render_template,after_this_request,current_app)
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import os


"""
TO DO:
Convert the html form data to use flask forms.
Style the html with Jinja templating and add a progress bar
for when the file is converted using jquery.
Add additional formats to convert to. As of now, wav is all that is needed.
Disallow a corrupt wav file from being uploaded, i.e., test.txt.wav.
As of now, this will cause internal server error. It won't crash flask,
but it's still ugly. Try/Except block didn't work.
May need to experiment with 'lame' conversion. 
"""

app = Flask(__name__)

# Set folder where uploaded wav files will be uploaded,
# and where the mp3 will be saved after conversion.
UPLOAD_FOLDER = '/path/to/folder/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def transform(text_file_contents):
    # Strips the .wav off of the file and creates a new filename with .mp3
    new_name = text_file_contents[:-4] + ".mp3"
    try:
        AudioSegment.from_wav(UPLOAD_FOLDER + text_file_contents).export(UPLOAD_FOLDER + new_name, format="mp3")
        return new_name
    except TypeError:
        print("File type is not a valid audio file format. Only accepts WAV files.")
        return render_template('index.html')

def delete_wav(wav):
    # After successful submission response, wav is deleted to save
    # on server space.
    os.remove(UPLOAD_FOLDER + wav)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/wav')
def form():
    dir = os.listdir(UPLOAD_FOLDER)
    # Checking if the list is empty or not
    if len(dir) == 0:
        print("Empty directory")
    else:
        print("Not empty directory")
    return render_template('index.html')

@app.route('/download/<filename>', methods=["GET"])
def download(filename):
    return render_template('download.html',value=filename)

@app.route('/transform', methods=["GET","POST"])
def transform_view():
    if request.method == 'POST':
        # Grabs the uploaded user file
        request_file = request.files['data_file']
        if not request_file:
            return "No file"
        # Checks that it is a wav file. There may be better ways to do this..
        elif request_file.filename.endswith('.wav'):
            filename = secure_filename(request_file.filename)
            request_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = transform(filename)
            delete_wav(filename)
            return redirect('/download/'+ result)
        else:
            return render_template('index.html')
    return "Success"

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    # This checks if the mp3 exists, and if so it serves it then
    # deletes it after download. If it does not exist, user is redirected
    # the main wav2mp3 submit page.
    file_path = UPLOAD_FOLDER + filename
    if os.path.exists(file_path):
        file_handle = open(file_path, 'r')
        @after_this_request
        def remove_file(response):
            try:
                os.remove(file_path)
                file_handle.close()
            except Exception as error:
                app.logger.error("Error removing or closing downloaded file handle", error)
            return response
        return send_file(file_path, as_attachment=True, download_name='')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    # For running it locally, leave as is. If deploying, adjust these settings
    # It is not recommended to run in debug mode in production.
    app.run(host='0.0.0.0', port=5000, debug=True)
