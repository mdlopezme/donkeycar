import os
import time
import subprocess
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = { 'zip' }

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def front_page():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file
        #  without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Process upload if file is allowed
        if file and allowed_file(file.filename):
            filename_nopath = secure_filename(file.filename)
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M', t)
            filename = timestamp + '_' + filename_nopath
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(file_path)
            return redirect(url_for('processing_file', name=filename_nopath, date_created=timestamp))

    return '''
    <!doctype html>
    <title>Donkeycar Trainer</title>
    <h1>Note: Zip the data folder</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/processing')
def processing_file():
    name  = request.args.get('name', None)
    date_created  = request.args.get('date_created', None)

    Flask.Respo
    p = subprocess.Popen( [ "./donkeytrain.sh", '-f', name, '-d', date_created] )
    p.wait()

    return redirect(url_for('download_file', name=name, date_created=date_created))

@app.route('/download')
def download_file():
    name  = request.args.get('name', None)
    date_created  = request.args.get('date_created', None)
    return send_file(f'models/{date_created}_{name[:-4]}.h5', as_attachment=True)