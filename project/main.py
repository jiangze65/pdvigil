# main.py
import threading
from datetime import datetime
import time
import numpy as np
import re
from .models import PhaseDots
from .models import WaveForm
from .models import PDWave
from . import db
import csv
from flask import Blueprint, render_template,request,current_app
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

class StoppableThread (threading.Thread):
    def __init__(self, target, name):
        super (StoppableThread, self).__init__(target = target, name = name)
        self._stop = threading.Event ()
    def run (self):
        while not self._stop.is_set ():
            time.sleep (1)
            print (threading.currentThread (). getName () + ':' + str (datetime.today ()))
    def stop (self):
        self._stop.set ()
    def stopped (self):
        return self._stop.isSet ()
def get_thread_by_name (name):
    threads = threading.enumerate ()
    for thread in threads:
        if thread.getName () == name:
            return thread
    return None

@main.route('/start')
def start ():
    name = "Acquisition"
    if name:
        if not get_thread_by_name (name):
            db.session.query(PDWave).delete()
            db.session.commit()
            with current_app.open_resource('static/wave_form.csv', "r") as f:
              Lines = f.readlines()
            for line in Lines:
            	row=line.split(',',2)
            	pdwave=PDWave(phase=int(row[0]), peak=int(row[1]), data=row[2].strip("\n"))
            	db.session.add(pdwave)
            db.session.commit()
            f.close
            th = StoppableThread (target = StoppableThread, name = name)
            th.start ()
    return render_template('profile.html', name="Data Acquisition Thread Started!")
	
@main.route ('/stop')
def stop ():
    name = "Acquisition"
    if name:
        thread = get_thread_by_name (name)
        if thread:
            thread.stop ()
    return render_template('profile.html', name="Data Acquisition Thread Stopped!")
	
@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)
	
@main.route("/chart")
@main.route("/chart", methods=['POST'])
@login_required
def chart():
	selected=0 
	if request.method == 'POST':
		try: 
			selected = int(request.form['pointSelected'])
		except:
			print("An exception occurred")
	#Phase chart
	t = np.arange (0.0, 2000.0, 10.0)
	s = 512*np.sin(2*np.pi*(t/2000.0))
	t = [round(x) for x in t]
	s = [round(x) for x in s]
	phase = []
	amplitude = []
	legend = 'PDChart'
	phaseDots=PDWave.query.all()
	
	for phaseDot in phaseDots:
		phase.append(phaseDot.phase)
		amplitude.append({'x': phaseDot.phase, 'y': phaseDot.peak})
	ugly_blob = re.sub("[']", '', str(amplitude))
	
	#Wavefrom
	xrange = np.arange (0, 512, 1)
	if(int(selected)>0):
		qs = PDWave.query.filter_by(phase=selected).first()	

	if(selected<1 or qs is None):
		qs = PDWave.query.first()
		
	yrange={qs.data}
	ugly_blob0 = str(yrange).replace("'", "")
	ugly_blob1= re.sub("[{]","[",ugly_blob0)
	ugly_blob2= re.sub("[}]","]",ugly_blob1)

	#FFT chart
	#qs = PDWave.queryfilter_by(phase=selected).first()
	yrange={qs.data}
	ugly_b = str(yrange).replace("'", "")
	ugly_b1= re.sub("[{]","",ugly_b)
	ugly_b2= re.sub("[}]","",ugly_b1)	
	list=ugly_b2.split(",")
	x = []
	for i in list:
		x.append(int(i))
	w = np.fft.fft(x)
	z =np.abs(w[0:256])
	fftVale="["
	for x in z:
		fftVale+=str(x)
		fftVale+=","
	fftVale+="]"
	#print(fftVale)
	return render_template('chart.html', values=ugly_blob, labels=s, phases=t,values2=ugly_blob2, labels2=xrange,values4=fftVale, labels4=50/256*xrange[0:256])
	
@main.route("/waveform")
@login_required
def waveform():
	xrange = np.arange (0, 512, 1)
	#qs = WaveForm.query.first()
	qs = PDWave.query.first()
	yrange={qs.data}
	ugly_blob = str(yrange).replace("'", "")
	ugly_blob1= re.sub("[{]","[",ugly_blob)
	ugly_blob2= re.sub("[}]","]",ugly_blob1)
	print(ugly_blob2)
	return rgender_template('waveform.html', values=ugly_blob2, labels=xrange,legend='WaveForm')
	
@main.route("/fftchart")
@login_required
def fftchart():
	xrange = np.arange (0, 512, 1)
	#qs = WaveForm.query.first()
	qs = PDWave.query.first()
	yrange={qs.data}
	ugly_blob = str(yrange).replace("'", "")
	ugly_blob1= re.sub("[{]","",ugly_blob)
	ugly_blob2= re.sub("[}]","",ugly_blob1)	
	list=ugly_blob2.split(",")
	x = []
	for i in list:
		x.append(int(i))
	w = np.fft.fft(x)
	z =np.abs(w[0:256])
	#freqs = np.fft.fftfreq(len(x))
	height="["
	for s in z:
		height+=str(s)
		height+=","
	height+="]"
	print(len(w))
	print(w)
	print("...............................")
	print(height)
	return render_template('waveform.html', values=height, labels=50/256*xrange[0:256],legend='FFTChart')