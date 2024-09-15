#! python3.7

import argparse
import socket
import threading

from datetime import datetime, timedelta
from time import sleep
from sys import platform
from functions import *

# Server configuration
HOST = 'localhost'  # Server's IP address
PORT = 9090        # Port to listen on

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="tiny", help="Model to use", choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true', help="Don't use the english model.")
    parser.add_argument("--energy_threshold", default=1000, help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2, help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3, help="How much empty space between recordings before we consider it a new line in the transcription.", type=float)
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse', help="Default microphone name for SpeechRecognition. Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()

    # The last time a recording was retrieved from the queue.
    phrase_time = None

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

    cleanup("audio")

    # Record audio in a separate thread
    record_audio(source, args.record_timeout)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout
    
    try:
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()

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
                process_audio_data(audio_data, phrase_complete)
                data_queue.queue.clear()

            else:
                # Infinite loops are bad for processors, must sleep.
                sleep(0.25)
    except KeyboardInterrupt:
        print("Server interrupted and shutting down.")
        print("\n\nTranscription:")
        for line in transcription:
            print(line)
    finally:
        s.close()
        print("\n\nTranscription:")
        for line in transcription:
            print(line)


if __name__ == "__main__":
    main()
