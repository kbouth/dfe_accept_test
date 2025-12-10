from cothread.catools import caget
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)


Frf = 499.68         #MHz
Fturn = Frf/1320.0   #MHZ
Fadc = Fturn*310.0   #MHz

dt = 1.0/Fadc
print(Fadc,dt)

Apv = "lab-BI{BPM:2}ADC:A:Buff-Wfm"
Bpv = "lab-BI{BPM:2}ADC:B:Buff-Wfm"
Cpv = "lab-BI{BPM:2}ADC:C:Buff-Wfm"
Dpv = "lab-BI{BPM:2}ADC:D:Buff-Wfm"

A = caget(Apv,timeout=10)
B = caget(Bpv)
C = caget(Cpv)
D = caget(Dpv)

L = len(A)
print(L)
T = dt*L
df = 1000.0*(1/T)  #Hz

H = np.hanning(L)
AO = np.subtract(A,np.mean(A))
BO = np.subtract(B,np.mean(B))
CO = np.subtract(C,np.mean(C))
DO = np.subtract(D,np.mean(D))
AH = np.multiply(AO,H)  
BH = np.multiply(BO,H)
CH = np.multiply(CO,H)  
DH = np.multiply(DO,H)
print(L,T,df)

TM=[]
for i in range(0,L):
   TM.append(i*dt)
   
F = []
for i in range(0,int(L/2)):
   F.append(i*df)

Afft = np.fft.fft(AH)/L
Afft = Afft[0:int(L/2)]
Afft = 2.0*np.abs(Afft)
Afft0 = Afft[0]
Afft[0] = 0

Bfft = np.fft.fft(BH)/L
Bfft = Bfft[0:int(L/2)]
Bfft = 2.0*np.abs(Bfft)
Bfft0 = Bfft[0]
Bfft[0] = 0

Cfft = np.fft.fft(CH)/L
Cfft = Cfft[0:int(L/2)]
Cfft = 2.0*np.abs(Cfft)
Cfft0 = Cfft[0]
Cfft[0] = 0

Dfft = np.fft.fft(DH)/L
Dfft = Dfft[0:int(L/2)]
Dfft = 2.0*np.abs(Dfft)
Dfft0 = Dfft[0]
Dfft[0] = 0
   

f,ax = plt.subplots(2,2,figsize=(10,10))

print(len(A))
Aavg = float(np.mean(A))
Asig = float(np.std(A))
ax[0][0].plot(TM,A)
ax[0][0].grid(True)
ax[0][0].set_xlabel("Time (mSec)")
ax[0][0].set_ylabel("Channel A")
dstr = "Aavg = "+str(round(Aavg,3))+"\nAsig = "+str(round(Asig,3))
ax[0][0].text(0.05, 0.95,dstr,transform=ax[0][0].transAxes, fontsize=12,verticalalignment='top', bbox=props)

Cavg = float(np.mean(C))
Csig = float(np.std(C))
ax[0][1].plot(TM,C)
ax[0][1].grid(True)
ax[0][1].set_xlabel("Time (mSec)")
ax[0][1].set_ylabel("Channel C")
dstr = "Cavg = "+str(round(Cavg,3))+"\nCsig = "+str(round(Csig,3))
ax[0][1].text(0.05, 0.95,dstr,transform=ax[0][1].transAxes, fontsize=12,verticalalignment='top', bbox=props)

ax[1][0].plot(F,Afft)
ax[1][0].grid(True)
ax[1][0].set_xlabel("Frequency (Hz)")
ax[1][0].set_ylabel("A Amplitude")
dstr = "df = "+str(round(df,3))+"Hz"
ax[1][0].text(0.6, 0.95,dstr,transform=ax[1][0].transAxes, fontsize=12,verticalalignment='top', bbox=props)

ax[1][1].plot(F,Cfft)
ax[1][1].grid(True)
ax[1][1].set_xlabel("Frequency (Hz)")
ax[1][1].set_ylabel("C Amplitude")
dstr = "df = "+str(round(df,3))+"Hz"
ax[1][1].text(0.6, 0.95,dstr,transform=ax[1][1].transAxes, fontsize=12,verticalalignment='top', bbox=props)

f,ax = plt.subplots(2,2,figsize=(10,10))

Bavg = float(np.mean(B))
Bsig = float(np.std(B))
ax[0][0].plot(TM,B)
ax[0][0].grid(True)
ax[0][0].set_xlabel("Time (mSec)")
ax[0][0].set_ylabel("Channel B")
dstr = "Bavg = "+str(round(Bavg,3))+"\nBsig = "+str(round(Bsig,3))
ax[0][0].text(0.05, 0.95,dstr,transform=ax[0][0].transAxes, fontsize=12,verticalalignment='top', bbox=props)

Davg = float(np.mean(D))
Dsig = float(np.std(D))
ax[0][1].plot(TM,D)
ax[0][1].grid(True)
ax[0][1].set_xlabel("Time (mSec)")
ax[0][1].set_ylabel("Channel D")
dstr = "Davg = "+str(round(Davg,3))+"\nDsig = "+str(round(Dsig,3))
ax[0][1].text(0.05, 0.95,dstr,transform=ax[0][1].transAxes, fontsize=12,verticalalignment='top', bbox=props)

ax[1][0].plot(F,Bfft)
ax[1][0].grid(True)
ax[1][0].set_xlabel("Frequency (Hz)")
ax[1][0].set_ylabel("B Amplitude")
dstr = "df = "+str(round(df,3))+"Hz"
ax[1][0].text(0.6, 0.95,dstr,transform=ax[1][0].transAxes, fontsize=12,verticalalignment='top', bbox=props)

ax[1][1].plot(F,Dfft)
ax[1][1].grid(True)
ax[1][1].set_xlabel("Frequency (Hz)")
ax[1][1].set_ylabel("D Amplitude")
dstr = "df = "+str(round(df,3))+"Hz"
ax[1][1].text(0.6, 0.95,dstr,transform=ax[1][1].transAxes, fontsize=12,verticalalignment='top', bbox=props)

plt.show()

