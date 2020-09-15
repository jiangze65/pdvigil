#WaveForm_FFT_FastPlot with Blit
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.fftpack import fft, rfft
import csv

PulseLength = 512
HfFFTlen = PulseLength//2
#print(HfFFTlen)
t = np.arange (0, PulseLength, 1)
yf = []

fig, (ax, ax2) = plt.subplots(1, 2, num='Pdvigil Technology Pte Ltd', figsize=(16, 8))
line1, = ax.plot(np.random.rand(PulseLength))
line2, = ax2.plot( 128 * PulseLength * np.random.rand(HfFFTlen)) # adjust X to match FFT magnitude
                  # - 128 for sine wave with about 256 amplitude, 8 for pulse of 480 amplitude
#line2, = ax2.semilogx(np.random.rand(HfFFTlen))
fig.suptitle('PDvigil1.11 Partial Discharge Monitoring and Analyzing System', fontsize=16)
ax.axis([0, PulseLength, -512, 512])
ax.set_xlabel("Time (unit: 10ns)")
ax.set_ylabel("Amplitude, Resolution = (1V/512)/Gain")
ax.set_title('Waveform')
#ax2.axis([0, PulseLength, 0, PulseLength])
ax2.set_title('Spectrum')
plt.show(block = False)

f = open("WvForm.csv", "r")

with f:
    csv_reader = csv.reader(f)
    pulse_count = 0
    for row in csv_reader:
        if pulse_count == 0:
            #print(row)
            pulse_count += 1
        else:
            y_fft = fft(row)
            y_mag = np.abs(y_fft[0 : HfFFTlen])
            #print("FFT #: ", pulse_count)
            #print(y_mag)
            
            line1.set_ydata(row)
            line2.set_ydata(y_mag)
            
            ax.draw_artist(ax.patch)
            ax2.draw_artist(ax2.patch)
            
            ax.draw_artist(line1)
            ax2.draw_artist(line2)
            
            fig.canvas.blit(ax.bbox)
            fig.canvas.blit(ax2.bbox)
            
            fig.canvas.flush_events()
            
            pulse_count += 1

f.close

print("Total number of pulses ploted: ", str(pulse_count-1))
print("Complete ploting waveforms successfully!")

