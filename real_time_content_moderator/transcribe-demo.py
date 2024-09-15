import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
import re
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
import ssl
import warnings
from flask import Flask, jsonify
import threading
import time
from flask_cors import CORS

ssl._create_default_https_context = ssl._create_unverified_context
warnings.filterwarnings("ignore", category=FutureWarning)
app = Flask(__name__)
CORS(app)
transcription = []
num_censored = 0

@app.route('/transcription', methods=['GET'])
def get_transcription():
    return jsonify({'transcription': transcription})

@app.route('/num-censored', methods=['GET'])
def get_num_censored():
    return jsonify({'num_censored': num_censored})

def replaceWord(line):
  global num_censored
  if re.compile(r'\b({0})\b'.format(line), flags=re.IGNORECASE).search:
      rep_line = re.sub('chocolate', 'goose', line)
      if rep_line != line:
        num_censored += 1
  return rep_line
    
def main():
    global transcription    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="base", help="Model to use",
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
                data_queue.queue.clear()
                
                # Convert in-ram buffer to something the model can use directly without needing a temp file.
                # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
                # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Read the transcription.
                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                # If we detected a pause between recordings, add a new item to our transcription.
                # Otherwise edit the existing one.
                if phrase_complete:
                    transcription.append(text)
                else:
                    transcription[-1] = text

                # Clear the console to reprint the updated transcription.
                os.system('cls' if os.name=='nt' else 'clear')
                # for line in transcription:
                #   line = replaceWord(line)
                #   transcription.append(line)
                #   print(line)
                for i in range(len(transcription)):
                    transcription[i] = replaceWord(transcription[i])
                    print(transcription[i])
                 
                # Flush stdout.
                print('', end='', flush=True)
            else:
                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
        except KeyboardInterrupt:
            break
          
if __name__ == "__main__":
    flask_thread = threading.Thread(target=lambda: app.run(port=5001, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    main()