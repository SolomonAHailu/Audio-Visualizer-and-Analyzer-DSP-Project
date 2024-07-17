















































import struct
import pyaudio
import matplotlib.pyplot
import numpy as np

#  VARIABLES
CHUNK = 1024*2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

#  OBJECTS/INSTANCES
p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

fig, (plot_one, plot_two) = matplotlib.pyplot.subplots(2, figsize=(5, 5))
x = np.arange(0, 2*CHUNK, 2)
x_fft = np.linspace(0, RATE, CHUNK)
line, = plot_one.plot(x, np.random.rand(CHUNK), '-', lw=1)
line_fft, = plot_two.semilogx(x_fft, (np.random.rand(CHUNK)), '-', lw=1)

# Plot parameters labels
plot_one.set_title("AUDIO VISUALIZATION\n")
plot_one.set_ylim(-500, 500)
plot_one.set_xlim(0, CHUNK)
plot_one.set_xlabel("Time")
plot_one.set_ylabel("Amplitude")
plot_one.grid()

plot_two.set_xlim(20, RATE/2)
plot_two.set_ylim(0, 0.01)
plot_two.set_xlabel("Frequency")
plot_two.set_ylabel("Magnitude")
plot_two.grid()

matplotlib.pyplot.tight_layout()
fig.show()

while True:
    data = stream.read(CHUNK)
    dataInt = struct.unpack(str(CHUNK) + 'h', data)
    line.set_ydata(dataInt)
    line_fft.set_ydata(np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK))
    fig.canvas.draw()
    fig.canvas.flush_events()
