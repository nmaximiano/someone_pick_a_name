import pyaudio
import numpy as np
import time
import json

# Set chunk size. Controls how long we sample.
CHUNK = 4096

# Initialize pyaudio.
p = pyaudio.PyAudio()
# Initialize stream. Pass values.
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, input_device_index=1, frames_per_buffer=CHUNK)

print("Listening for volume level... (Press Ctrl+C to stop)")

def write_data(file_name : str, data : dict):
    # Open file in read-write mode.
    with open(file_name, "r+") as file:
        json_data = json.load(file)
        json_data[data["timestamp"]] = data
        
        file.truncate(0)
        file.seek(0)
        file.write(json.dumps(json_data))    

try:
    average = []
    while True:
        data = stream.read(CHUNK)  # Read audio data
        audio_array = np.frombuffer(data, dtype=np.int16)  # Convert to numpy array
        rms = np.sqrt(np.mean(audio_array.astype(np.float32) ** 2))  # Compute RMS volume
        db = 20 * np.log10(rms + 1e-10)  # Convert to dB, avoiding log(0)

        average.append(db)
        if len(average) > 360:
            write_data("data/volume_level.json", {"timestamp" : time.time(), "average": sum(average) / len(average)})
            average = []
            continue
        print(f"Volume Level: {db:.2f}")


except KeyboardInterrupt:
    print("Stopping...")

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
