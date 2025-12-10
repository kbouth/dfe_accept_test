import matplotlib.pyplot as plt
from cothread.catools import caget

A = caget("lab-BI{BPM:2}ADC:A:Buff-Wfm")

plt.plot(A)
plt.show()
