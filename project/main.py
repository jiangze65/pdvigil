# main.py
from datetime import datetime
import time
import numpy as np
import re
from .models import PhaseDots
from .models import WaveForm
from .models import PDWave
from . import db
import csv,json
from flask import Blueprint, render_template,request,current_app
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')
	
@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)
	
@main.route("/chart") #press a navigation bar
@main.route("/chart", methods=['POST']) #post request from anywhere
@login_required
def chart():
	selected=0 
	if request.method == 'POST':
		try: 
			selected = int(request.form['pointSelected'])
		except:
			print("An exception occurred")
			
	data = {}
	#Phase chart
	t = np.arange (0, 2000, 1)
	data['pdchart_label'] = t.tolist();
	s = 512*np.sin(2*np.pi*(t/2000.0))
	s = [round(x) for x in s]
	data['pdchart_data'] = s;
	
	datax = []
	datay = []
	pdchart_data = []
	phaseDots=PDWave.query.all()
	for phaseDot in phaseDots:
		datax.append(phaseDot.phase)
		datay.append(phaseDot.peak)
	data['pdchart_plotx'] = datax
	data['pdchart_ploty'] = datay

	#Waveform
	xrange = np.arange (0, 512, 1)
	data['wvchart_label'] = xrange.tolist();
	if(int(selected)>0):
		qs = PDWave.query.filter_by(phase=selected).first()	

	if(selected<1 or qs is None):
		qs = PDWave.query.first()
		
	yrange={qs.data}
	results = str(yrange)[2:-2].split(",")
	data['wvchart_data'] = results
		
	#FFT chart
	w = np.fft.fft(list(map(int, results))) #convert to integer first before FFT
	z =np.abs(w[0:256]) #FFT result

	data['fftchart_label'] = xrange[0:256].tolist()
	data['fftchart_data'] = z.tolist()
	
	#print(data)
	json_data = json.dumps(data)
	return render_template('multichart.html', data=json_data)
	
@main.route("/waveform")
@login_required
def waveform():
	xrange = np.arange (0, 512, 1)
	qs = PDWave.query.first() #read first record from the table
	yrange={qs.data}
	print(yrange)
	results = list(map(int, str(yrange)[2:-2].split(",")))
	print(results)
	return render_template('waveform.html', values=results, labels=xrange,legend='WaveForm')
	
@main.route("/fftchart")
@login_required
def fftchart():
	xrange = np.arange (0, 512, 1)
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
	height="["
	for s in z:
		height+=str(s)
		height+=","
	height+="]"
	return render_template('waveform.html', values=height, labels=50/256*xrange[0:256],legend='FFTChart')
@main.route("/config")
@login_required
def config():
	data = {"device_status":"Stopped", 
		"sn":"XXXXXXXXXXXXXXXXXXXXXXXX", 
		"key":"YYYYYYYYYYYYYYYYYYYYYYY",
		"amplifier_gain":11,
		"pulse_length":512,
		"trigger_level": 61,
		"trigger_points": 54};
	return render_template('config.html',data=data)