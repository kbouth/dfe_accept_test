import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from time import sleep
from cothread.catools import caget

FApv = "lab-BI{BPM:2}FFT:Magnitude-Wfm"
TCpv = "lab-BI{BPM:2}EVR:Trig:Cnt-I"

rm = visa.ResourceManager()

dev = 'TCPIP0::10.0.142.183::5025::SOCKET'
source = rm.open_resource(dev)
print('\nRF Source TCPIP Open Successful!')
source.read_termination = '\n'
source.write_termination = '\n'
response = source.query('*IDN?')
print(response[35:42])
serial_number = int(response[35:41])
if(serial_number != 102463):
    print('R&S SMB100B Source NOT FOUND...exiting!')
    exit()
else:
    print('R&S SMB100B Source FOUND.')

source.write("FREQ 499.68e6")
source.write("POW 0.09V")
source.write("OUTP ON")

fig,ax = plt.subplots(1,1)
plt.ion()

F = []
P = []
for i in range(0,100):
   fmod = 50 + i*100
   F.append(fmod/1000.0)
   source.write("LFO:FREQ "+str(fmod))
   print(i,fmod)
   sleep(7)
   count = 0
   Psum = 0
   oldTC = caget(TCpv)
   while count<10:
      TC = caget(TCpv)
      if(TC==oldTC):
         sleep(0.5)
      else:
         count = count + 1
         FFT = np.array(caget(FApv))
         maxIndx = np.argmax(FFT)
         FFTsum=0
         for j in range((maxIndx-5),maxIndx+5):
            FFTsum = FFTsum + FFT[j]
         Psum = Psum + FFTsum
         print(Psum/count)
         oldTC = TC
   P.append(Psum/10000.0)

   ax.clear()  
   ax.plot(F,P,'-o')
   ax.grid(True)
   ax.set_xlabel('Frequency (KHz)')
   ax.set_ylabel('Amplitude (AU)') 
   plt.pause(0.01) 


