#! python3.7

import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
import re
import wave
import socket
import threading

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform, getsizeof
from pydub import AudioSegment
from io import BytesIO

# Server configuration
HOST = 'localhost'  # Server's IP address
PORT = 9090        # Port to listen on
CHUNK_SIZE = 1024

ban_word = "chocolate"
buffer = BytesIO(b"")

def handle_client(conn):
    """Handle client connection in a separate thread."""
    buffer_audio(conn)
    conn.close()

def replaceWord(line):
    rep_line = line
    if re.compile(r'\b({0})\b'.format(line), flags=re.IGNORECASE).search:
        rep_line = re.sub(ban_word, 'wolf', line)
    return rep_line

def replace_audio(og_file, start_time, end_time, rep_file="rep/bleep.wav"):
    # Load the original audio and replacement audio
    og_audio = AudioSegment.from_file(og_file)
    rep_audio = AudioSegment.from_file(rep_file)

    # Convert timestamps (seconds) to milliseconds
    start_time_ms = start_time * 1000
    end_time_ms = end_time * 1000

    # Split the original audio into three parts
    before_segment = og_audio[:start_time_ms]  # Before the segment to replace
    after_segment = og_audio[end_time_ms:]     # After the segment to replace
    rep_audio_segment = rep_audio[start_time_ms:end_time_ms]    # Segment to replace with

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="tiny", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()

    # The last time a recording was retrieved from the queue.
    phrase_time = None
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    # Important for linux users.
    # Prevents permanent application hang and crash by using the wrong Microphone
    if 'linux' in platform:
        mic_name = args.default_microphone
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    source = sr.Microphone(sample_rate=16000, device_index=index)
                    break
    else:
        source = sr.Microphone(sample_rate=16000)

    # Load / Download model
    model = args.model
    if args.model != "large" and not args.non_english:
        model = model + ".en"
    audio_model = whisper.load_model(model)

    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout

    transcription = ['']

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio:sr.AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    # Cue the user that we're ready to go.
    print("Model loaded.\n")

    # cleanup("audio")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    # s.settimeout(60)  # Set a timeout for the socket

    try:
        while True:
            try:
                now = datetime.utcnow()
                # Pull raw recorded audio from the queue.
                if not data_queue.empty():
                    phrase_complete = False
                    # If enough time has passed between recordings, consider the phrase complete.
                    # Clear the current working audio buffer to start over with the new data.
                    if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    phrase_time = now
                    
                    # Combine audio data from queue
                    audio_data = b''.join(data_queue.queue)
                    save_audio_wf(audio_data)
                    data_queue.queue.clear()
                    
                    # Convert in-ram buffer to something the model can use directly without needing a temp file.
                    # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                    # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                    # Read the transcription.
                    result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available(), word_timestamps=True)
                    text = result['text'].strip()
                    # Look for the banned word and print the timestamp
                    for segment in result['segments']:
                        for i, word in enumerate(segment['words']):
                            if re.search(r'\bchocolates?\b', word['word'], re.IGNORECASE):
                                # Fetch the previous and next words safely
                                prev_word = segment['words'][i - 1] if i > 0 else None
                                next_word = segment['words'][i + 1] if i < len(segment['words']) - 1 else None
                                
                                # Calculate start_time
                                if prev_word is None:
                                    start_time = 0.0
                                else:
                                    start_time = prev_word['end']
                                
                                # Calculate end_time
                                if next_word is None:
                                    end_time = word['end']
                                else:
                                    end_time = next_word['start']
                                files = os.scandir("audio")
                                latest_file = max(files, key=os.path.getctime)
                                replace_audio(latest_file, start_time, end_time)
                                with open("stamps.txt", "a") as f:
                                    f.write(f"Found at {start_time:.2f}s to {end_time:.2f}s in {latest_file}\n")
                                    f.close()
                                # print(f"Found at {start_time:.2f}s in {latest_file}")

                    # If we detected a pause between recordings, add a new item to our transcription.
                    # Otherwise edit the existing one.
                    if phrase_complete:
                        transcription.append(text)
                    else:
                        transcription[-1] = text

                    # Clear the console to reprint the updated transcription.
                    # os.system('cls' if os.name=='nt' else 'clear')
                    for line in transcription:
                        new_line = replaceWord(line)
                        transcription[transcription.index(line)] = new_line
                        print(new_line)
                    # Flush stdout.
                    print('', end='', flush=True)
                else:
                    # Infinite loops are bad for processors, must sleep.
                    sleep(0.25)
                    conn, addr = s.accept()
                    print(f"Connected by {addr}")

                    # Start a new thread to handle the client
                    client_thread = threading.Thread(target=handle_client, args=(conn,))
                    client_thread.start()

            except KeyboardInterrupt:
                break
            except ConnectionRefusedError:
                print("Connection closed by client")
    finally:
        s.close()
        print("\n\nTranscription:")
        for line in transcription:
            print(line)


if __name__ == "__main__":
    main()
