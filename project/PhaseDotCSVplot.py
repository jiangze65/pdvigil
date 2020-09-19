import matplotlib.pyplot as plt
import numpy as np

t = np.arange (0.0, 2000.0, 10.0)
s = 512*np.sin(2*np.pi*(t/2000.0))

phase = []
amplitude = []

f = open("PhaseDots.csv", "r")

with f:
    for row in csv_reader:
        if line_count == 0:
            print(row)
            line_count += 1
        else:
            print(row[1: ])
            phase.append(row[1])
            amplitude.append(row[2])
            line_count += 1

f.close

print(phase)
print(amplitude)
print("Total number of pulses: ", str(line_count-1)) 

#plt.plot(t, 0.0*t, t, s, phase, amplitude, 'bo')
plt.figure(num='Pdvigil Technology Pte Ltd', figsize=(16, 8))
plt.plot(t, 0.0*t)
plt.plot(t, s)
#plt.plot(phase, amplitude, 'bo')
plt.scatter(phase, amplitude, s=4)
plt.axis([0, 2000, -512, 512])
plt.xlabel("Cycle Time unit: us)")
plt.ylabel("Pulse Peak, Resolution = (1V/512)/Gain")
plt.title('PDvigil1.11 Partial Discharge Monitoring and Analyzing System', fontsize=16)
#plt.show(block = False)
plt.show()
print("Total number of pulses ploted: ", str(line_count-1))
print("Plot completed successfully!")
