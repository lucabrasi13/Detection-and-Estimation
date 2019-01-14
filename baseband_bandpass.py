import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert,butter
from scipy.signal import filtfilt
import warnings

##------------------------------Function declaration----------------------------##
def delayed_cosine_pulse(t):
	""" Function to generate the Delayed Cosine pulse 
	:param: t: Time constraint
	:return
	"""

	arc = (np.pi*(t-tdrc))/(Tzrc/2)
	return Arc*(np.cos(brc*arc)/(1-(((2/np.pi)*brc*arc)**2))*(np.sin(arc)/arc))

def gen_analytic_signal(s):
	""" Function to genrate the corresponding Analytic signal
	:param: s: Real signal
	"""	

	return hilbert(s)

def gen_bandpass_signal(sA,w0,t):
	""" Function to create a bandpass signal from the Analytic signal
	:param:	sA: Analytic signal
	:param: w0: Angular freq
	:return: 
	"""

	I = np.real(sA)
	Q = np.imag(sA)
	return I*np.cos(w0*t) - Q*np.sin(w0*t)

def bandpass_to_baseband(sbp,w0,t):
	""" Function to convert Bandpass to Baseband signal
	:param: sbp: Bandpass signal
	:return:
	"""

	return sbp*np.sqrt(2)*np.cos(w0*t),sbp*-np.sqrt(2)*np.sin(w0*t)

def LPF(Fc,Ihat,Qhat):
	""" Function to filter the demodulated signal
	:param Fc: Cutoff freq
	:return
	"""

	b,a = butter(NFILT,Fc)
	return filtfilt(b,a,Ihat),filtfilt(b,a,Qhat)
	
##------------------------------Global variable declaration --------------------##
global T
global tdrc
global Tzrc
global Arc
global brc
global Ts
global NFILT

##------------------------------Global variable definition ---------------------##

T = 1
tdrc = T/2
Tzrc = T/2
Arc = 1
brc = 0.25
Ts = 0.005*T
w0 = 2*np.pi*(0.1/Ts)
NFILT = 6
 
## Generate the signal to be transmitted
t = np.linspace(-T,2*T,1000)
np.seterr(divide='ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)
x = delayed_cosine_pulse(t)
index = np.argwhere(np.isinf(x))
x = np.delete(x,index)
t = np.delete(t,index)

## Generate the Analytical signal
y = gen_analytic_signal(x)

## Generate the bandpass signal
sbp = gen_bandpass_signal(y,w0,t)

## Signal demodulation
Ihat,Qhat = bandpass_to_baseband(sbp,w0,t)

## Low pass filtering
Fc = (w0/(2*np.pi))/(1/Ts)
IhatL,QhatL = LPF(Fc,Ihat,Qhat)

## Plot the results
plt.figure()
plt.plot(t,np.real(y),'b-',label='I component')
plt.plot(t,np.imag(y),'g--',label='Q component')
plt.grid(True)
plt.legend()
plt.title('Baseband signal')
plt.xlabel('Time(s) -->')
plt.ylabel('Amplitude -->')
plt.figure()
plt.plot(t,sbp)
plt.grid(True)
plt.title('Bandpass signal')
plt.xlabel('Time(s) -->')
plt.ylabel('Amplitude -->')
plt.figure()
plt.subplot(2,2,1)
plt.plot(t,Ihat,'b-')
plt.title('I with/without LPF')
plt.grid(True)
plt.subplot(2,2,2)
plt.plot(t,Qhat,'g--')
plt.title('Q with/without LPF')
plt.grid(True)
plt.subplot(2,2,3)
plt.plot(t,IhatL,'b-')
plt.grid(True)
plt.subplot(2,2,4)
plt.plot(t,QhatL,'g-')
plt.grid(True)
plt.show()












