import subprocess
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
from datetime import timedelta
import shutil
import os
import io
import tempfile
import json
import time




app = Flask(__name__)
app.config["SECRET_KEY"] = "Qrawler123456"
CORS(app)
production=True




if production:
    socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*", async_mode="eventlet", always_connect=True)
else:
    socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*",always_connect=True)





bucket_name = 'qrawler-10df1.appspot.com'
root_path = os.path.dirname(os.path.abspath(__file__))



# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate('./keys/serviceAccount.json')
    firebase_admin.initialize_app(cred, {'storageBucket': bucket_name})
except Exception as e:
    socketio.emit('error', str(e))  # Emit initialization error to the client
    raise





@socketio.on('connect')
def handle_connect():
    send("Hey, from the server.")






@socketio.on('disconnect')
def handle_disconnect():
    send("Opps! you are disconnected.")





@app.route('/', methods=['GET'])
def handle_server_test():
    return jsonify({'status': 200, 'message': 'Server working fine'}), 200






@app.route('/process/v1/downloads', methods=['POST'])
def handle_upload():
    try:
        data = request.get_json()
        user_id = data.get('userId')
        software_id = data.get('softwareId')
        software_version = data.get('softwareVersion')
        if user_id and software_id and software_version:
            socketio.emit('progress_update', "Initializing file conversion...")
            # Read the template file
            template_file_path = os.path.join(root_path, 'inputs','qrawler.py')

            output_dir=''
            # Create a temporary directory for the output files
            with tempfile.TemporaryDirectory() as temp_dir:
                output_dir = os.path.join(temp_dir, 'outputs', user_id)
                
        
            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            template=''
            with open(template_file_path, 'r') as template_file:
                template = template_file.read()
            
            # Replace placeholders in the template with the values
            replaced_template = template.replace('_softwareId_', software_id).replace('_softwareVersion_', software_version)
            # Write the replaced template to the output file
            output_file_path = os.path.join(output_dir, 'qrawler.py')
            with open(output_file_path, 'w') as output_file:
                output_file.write(replaced_template)
            
            
            # Change the current working directory to the output directory
            os.chdir(output_dir)
           

            socketio.emit('progress_update', "Initializing pyinstaller")
            
            # Run the conversion process using PyInstaller
            cmd = ['pyinstaller', 'qrawler.py', '--onefile']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            conversion_success = False
            while process.poll() is None:
                line = process.stdout.readline().decode().strip()
                socketio.emit('progress_update', line)  # Emit progress update to the client 
                
                if "Building EXE from EXE-00.toc completed successfully" in line:
                    socketio.emit('conversion_success', "Build completed successfully")  # Emit progress update to the client 
                    conversion_success = True
                    
            socketio.emit('progress_update', "Finalizing...")
            
            
            # Check if the file exists before uploading
            exe_file_path = os.path.join(output_dir, 'dist', 'qrawler.exe')
            download_url=''
            #Upload the executable file to Firebase Storage
            storage_client = firebase_admin.storage.bucket(bucket_name)
            destination_blob_name = f'downloads/{user_id}/qrawler.exe'
            blob = storage_client.blob(destination_blob_name)
            blob.upload_from_filename(exe_file_path, timeout=600)

            socketio.emit('progress_update', "Generating download URL...")
            # Get the download URL of the uploaded file
            download_url = blob.generate_signed_url(
                version='v4',
                expiration=timedelta(minutes=15),
                method='GET'
            )
            socketio.emit('progress_update', "Download URL generated successfully.")
                
                
                
                
            # # Delete the output directory
            if os.path.exists(output_dir):
                # Delete the output directory
                # Get the parent directory
                os.chdir(root_path)
                parent_dir = os.path.dirname(os.path.dirname(output_dir))
                def onerror(func, path, exc_info):
                    """
                    Error handler for shutil.rmtree that handles permission errors by ignoring them.
                    """
                    if isinstance(exc_info[1], PermissionError):
                        pass  # Ignore the error and continue deleting other files
                    else:
                        raise  # Re-raise the exception for other error types
                    
                time.sleep(1)
                shutil.rmtree(output_dir, onerror=onerror)
                shutil.rmtree(os.path.join(parent_dir,'outputs'), onerror=onerror,ignore_errors=True)
                shutil.rmtree(parent_dir, onerror=onerror,ignore_errors=True)

            

            return jsonify({'message': 'File prepared successfully.', 'download_url': download_url}), 200
            
        else:
            return jsonify({'message': 'Invalid request data.'}), 400
    except Exception as e:
        # Change the current working directory back to the root directory
        os.chdir(root_path)
        socketio.emit('error', str(e))  # Emit error to the client
        raise






@app.route('/process/v1/downloads/download', methods=['GET'])
def download_file():
    try:
        download_url = request.args.get('download_url')
        if download_url:
            try:
                response = requests.get(download_url)
                if response.status_code == 200:
                    file_contents = response.content
                    return send_file(
                        io.BytesIO(file_contents),
                        mimetype='application/octet-stream;charset=utf-8',
                        as_attachment=True,
                        download_name='qrawler.exe'
                    )
                else:
                    return 'Failed to download the file.'
            except requests.exceptions.RequestException as e:
                socketio.emit('error', str(e))  # Emit error to the client
                return 'Failed to download the file.'
        return 'Download URL is missing.'
    except Exception as e:
        # Change the current working directory back to the root directory
        os.chdir(root_path)
        socketio.emit('error', str(e))  # Emit error to the client
        raise






if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    socketio.run(app, host='0.0.0.0', port=port, debug=True, threaded=True)