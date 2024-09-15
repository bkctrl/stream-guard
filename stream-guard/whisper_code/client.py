import socket
import pyaudio

# Client configuration
HOST = 'localhost'  # Server's IP address
PORT = 8080        # Port to connect to

# Audio configuration
CHUNK_SIZE = 1024  # How much data to read at once (in bytes)
FORMAT = pyaudio.paInt16  # Format of the audio
CHANNELS = 1  # Mono audio
RATE = 16000  # 16kHz

def play_audio_stream():
    p = pyaudio.PyAudio()

    # Open a stream for audio output
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    # Continuously receive data from the server and play it
    try:
        print("Connected to server, receiving audio...")
        while True:
            data = s.recv(CHUNK_SIZE)
            if not data:
                print("Nothing here")
                continue
            if (len(data) > 0):
                print(f"Received chunk of size: {len(data)} bytes")
                stream.write(data)  # Play audio as it arrives
    except Exception as e:
        print(f"An error occurred: {e}")
    # Cleanup
    s.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    play_audio_stream()
