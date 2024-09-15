### Imports ###
import os
import wave
import re
import numpy as np
import whisper
import torch
import argparse
import socket
import threading

from pydub import AudioSegment
from io import BytesIO
from queue import Queue
import speech_recognition as sr
from datetime import datetime, timedelta
from time import sleep
from sys import platform

### Variables ###
buffer = BytesIO(b"")
ban_word = "chocolate"
rep_word = "wolf"
data_queue = Queue()
transcription = ['']
CHUNK_SIZE = 1024
phrase_timeout = 3
record_timeout = 2

# Server configuration
HOST = 'localhost'  # Server's IP address
PORT = 8080        # Port to listen on

### Functions ###
def get_latest_name(filepath = "audio/output-wf-"):
    # Ensure the directory exists
    directory = os.path.dirname(filepath)
    os.makedirs(directory, exist_ok=True)

    for i in range(100):
        fp = filepath + "%0.2d" % i + ".wav"
        if not os.path.isfile(fp):
            return fp
    fp = filepath + "00.wav"
    return fp

def save_audio_wf(audio_data, filename=None):
    if filename is None:
        filename = get_latest_name()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # mono
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(16000)  # 16kHz sample rate
        wf.writeframes(audio_data)

def buffer_audio(conn, audio_dir="audio"):
    sent_files = set()  # Keep track of files that have been sent
    
    # Get all the files in the directory and sort them
    files = sorted(os.listdir(audio_dir))
    
    # Iterate over the files and send the ones that haven't been sent yet
    for filename in files:
        if filename.endswith(".wav") and filename not in sent_files:
            try:
                # Mark the file as sent before actually sending it to avoid duplication
                sent_files.add(filename)
                
                # Send the new file
                print(f"Buffering: {filename}")
                file_path = os.path.join(audio_dir, filename)
                with wave.open(file_path, 'rb') as wf:
                        data = wf.readframes(wf.getnframes())
                        if len(data) > 0:
                            buffer.write(data)
                            if len(buffer.getvalue()) >= CHUNK_SIZE:
                                conn.sendall(buffer.getvalue())
                                print(f"Sent: {filename}")
                                buffer.truncate(0)
                                buffer.seek(0)
            except wave.Error as e:
                print(f"Error reading file {filename}: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    # Send any remaining data in the buffer
    if len(buffer.getvalue()) > 0:
        conn.sendall(buffer.getvalue())
        buffer.truncate(0)
        buffer.seek(0)        

def continuous_record_transcribe(source, record_timeout):
    """Continuously records and transcribes audio in the background."""
    record_audio(source, record_timeout)
    now = datetime.utcnow()
    # The last time a recording was retrieved from the queue.
    phrase_time = now
    while True:
        if not data_queue.empty():
            phrase_complete = False
            # If enough time has passed between recordings, consider the phrase complete.
            # Clear the current working audio buffer to start over with the new data.
            if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                print("Data entry")
                phrase_complete = True
            # This is the last time we received new audio data from the queue.
            phrase_time = now
            audio_data = data_queue.get()
            print("Processing audio data.")
            process_audio_data(audio_data, phrase_complete)
            data_queue.queue.clear()
        else:
            # Infinite loops are bad for processors, must sleep.
            sleep(0.25)

def server_thread():
    """Run the server to handle client connections."""
    # Start the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()  # Accept client connection
            print(f"Connected by {addr}")
            
            # Handle the client connection in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()

def handle_client(conn, audio_dir="audio"):
    """Handle client connection in a separate thread."""

    sent_files = set()  # Keep track of files that have been sent
    
    # Get all the files in the directory and sort them
    files = sorted(os.listdir(audio_dir))
    
    # Iterate over the files and send the ones that haven't been sent yet
    for filename in files:
        if filename.endswith(".wav") and filename not in sent_files:
            try:
                # Mark the file as sent before actually sending it to avoid duplication
                sent_files.add(filename)
                
                # Send the new file
                print(f"Buffering: {filename}")
                file_path = os.path.join(audio_dir, filename)
                with wave.open(file_path, 'rb') as wf:
                        data = wf.readframes(wf.getnframes())
                        if len(data) > 0:
                            buffer.write(data)
                            if len(buffer.getvalue()) >= CHUNK_SIZE:
                                conn.sendall(buffer.getvalue())
                                print(f"Sent: {filename}")
                                buffer.truncate(0)
                                buffer.seek(0)
                print(f"Sent: {filename}")
            except wave.Error as e:
                print(f"Error reading file {filename}: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")
    print("Client connected.")
    conn.close()
    print("Client disconnected.")

def record_audio(source, record_timeout):
    """Record audio from the microphone and push it to the queue."""
    recorder = sr.Recognizer()
    recorder.energy_threshold = 1000
    recorder.dynamic_energy_threshold = False

    def record_callback(_, audio: sr.AudioData) -> None:
        """Callback function to handle recorded audio."""
        data = audio.get_raw_data()
        data_queue.put(data)
        print("Audio data added to queue.")

    with source:
        recorder.adjust_for_ambient_noise(source)
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

def process_audio_data(audio_data, phrase_complete=False):
    """Process audio data and perform transcription using Whisper."""
    
    save_audio_wf(audio_data)
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    
    # Load model and transcribe audio
    model = whisper.load_model("tiny")  # Adjust based on user input
    result = model.transcribe(audio_np, fp16=torch.cuda.is_available(), word_timestamps=True)
     # Cue the user that we're ready to go.
    print("Model loaded.\n")
    text = result['text'].strip()

    # Look for the banned word and handle replacements
    for segment in result['segments']:
        for i, word in enumerate(segment['words']):
            if re.search(r'\bchocolates?\b', word['word'], re.IGNORECASE):
                # Fetch the previous and next words safely
                prev_word = segment['words'][i - 1] if i > 0 else None
                next_word = segment['words'][i + 1] if i < len(segment['words']) - 1 else None
                
                # Calculate start_time
                start_time = prev_word['end'] if prev_word else 0.0
                
                # Calculate end_time
                end_time = next_word['start'] if next_word else word['end']
                
                # Process the replacement
                files = os.scandir("audio")
                latest_audio = max(files, key=os.path.getctime)
                replace_audio(latest_audio, start_time, end_time)
                with open("stamps.txt", "a") as f:
                    f.write(f"Found at {start_time:.2f}s to {end_time:.2f}s in {latest_audio}\n")
                    f.close()
    # If we detected a pause between recordings, add a new item to our transcription.
    # Otherwise edit the existing one.
    if phrase_complete:
        transcription.append(text)
    else:
        transcription[-1] = text
    
    # Clear the console to reprint the updated transcription.
    os.system('cls' if os.name=='nt' else 'clear')
    for line in transcription:
        new_line = replace_word(line)
        transcription[transcription.index(line)] = new_line
        print(new_line)
        with open("transcript.txt", "a") as f:
            f.write(f"{new_line}\n")
            f.close()
    # Flush stdout.
    print('', end='', flush=True)

def replace_word(line):
    """Replace a word in the transcription with a replacement word."""
    rep_line = line
    if re.compile(r'\b({0})\b'.format(line), flags=re.IGNORECASE).search:
        rep_line = re.sub(ban_word, rep_word, line)
    return rep_line

def replace_audio(og_file, start_time, end_time, rep_file="rep/bleep.wav"):
    """Replace a segment in the audio file with a replacement audio."""
    # Load the original audio and replacement audio
    og_audio = AudioSegment.from_file(og_file)
    rep_audio = AudioSegment.from_file(rep_file)

    # Convert timestamps (seconds) to milliseconds
    start_time_ms = start_time * 1000
    end_time_ms = end_time * 1000

    # Split the original audio into three parts
    before_segment = og_audio[:start_time_ms]  # Before the segment to replace
    after_segment = og_audio[end_time_ms:]     # After the segment to replace
    rep_audio_segment = rep_audio[:end_time_ms - start_time_ms]    # Segment to replace with

    # Combine the audio: before + replacement + after
    new_audio = before_segment + rep_audio_segment + after_segment

    # Export the modified audio to a new file
    new_audio.export(og_file, format="wav")

def cleanup(directory_path):
   try:
     with os.scandir(directory_path) as entries:
       for entry in entries:
         if entry.is_file():
            os.unlink(entry.path)
     stamps_file = os.path.join(os.path.dirname(directory_path), "stamps.txt")
     if os.path.exists(stamps_file):
         os.unlink(stamps_file)
    #  print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")