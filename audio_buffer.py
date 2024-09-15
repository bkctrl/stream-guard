import pyaudio
import numpy as np
import time
from collections import deque

DELAY = 5                 # Delay in seconds
CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100              # Sampling rate (samples per second)
CHUNK = 1024              # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)

p = pyaudio.PyAudio()
buffer = deque(maxlen=int(RATE / CHUNK * DELAY))
stream_in = p.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)
stream_out = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

print("Recording and playing with a delay of {} seconds...".format(DELAY))

try:
    while True:
        # Read audio data from the microphone
        data = stream_in.read(CHUNK)
        
        # Convert the byte data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Append the audio data to the buffer
        buffer.append(audio_data)
        
        # If the buffer is full, output the oldest audio data
        if len(buffer) == buffer.maxlen:
            delayed_data = buffer.popleft()
            stream_out.write(delayed_data.tobytes())
        
except KeyboardInterrupt:
    print("Stopping...")

finally:
    # Close the streams
    stream_in.stop_stream()
    stream_in.close()
    stream_out.stop_stream()
    stream_out.close()
    
    # Terminate PyAudio
    p.terminate()

print("Stopped.")
