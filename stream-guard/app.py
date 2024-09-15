from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import time
import threading
import os
from  whisper_code.functions import get_transcript, transcription

app = Flask(__name__)

# Allow cross-origin requests from React
CORS(app)

transcript = get_transcript()

# Example route to handle data receiving
@app.route('/api/receive', methods=['POST'])
def receive_data():
    data = request.json
    # Process the data
    response = {'message': 'Data received successfully', 'received_data': data}
    return jsonify(response)

@app.route('/api/audio-list', methods=['GET'])
def get_audio_list():
    try:
        files = [f for f in os.listdir("tmp/") if os.path.isfile("tmp/"+ f)]
        return jsonify(files)
    except Exception as e:
        return str(e), 500

@app.route('/api/audio/<filename>', methods=['GET'])
def get_audio(filename):
    file_path = "tmp/" + filename
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='audio/wav')  # Adjust MIME type if needed
    else:
        return "File not found", 404

# Example route to send data to the React front-end
@app.route('/transcription', methods=['GET'])
def send_data():
    global transcript
    data = {'status':'success', 'message': transcript}
    return jsonify(data)

# Function to update data periodically by calling get_dynamic_data()
def update_data_periodically():
    global transcript
    while True:
        time.sleep(2)  # Update every 2 seconds
        # Call the function and update the global variable with the result
        transcript = get_transcript()
        print(f"Data updated: {transcript}")

if __name__ == '__main__':
    # Start the background thread to update transcription data
    update_thread = threading.Thread(target=update_data_periodically, daemon=True)
    update_thread.start()

    app.run(debug=True)