import socket
import pyaudio

# Client configuration
HOST = 'localhost'  # Server's IP address
PORT = 9090        # Port to connect to

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

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        # s.settimeout(60)  # Client waits for up to 30 seconds for data
        print("Connected to server, receiving audio...")
        
        # Continuously receive data from the server and play it
        while True:
            try:
                data = s.recv(CHUNK_SIZE)
                # if not data:
                #     print("Nothing here")
                #     break
                print("Data found")
                stream.write(data)  # Play audio as it arrives
            except KeyboardInterrupt:
                break

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    play_audio_stream()
