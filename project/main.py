# main.py
from datetime import datetime
import time
import numpy as np
import re
from .models import PhaseDots
from .models import WaveForm
from .models import PDWave
#from . import socketio
from . import db
import csv,json
from flask import Blueprint, render_template,request,current_app,session, jsonify
from flask_login import login_required, current_user
#from flask_socketio import emit, join_room, leave_room

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')
	
@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)
	
@main.route("/chart") #press a navigation bar
@login_required
def chart():
	return render_template('multichart.html')
@main.route("/waveform")
@login_required
def waveform():
	xrange = np.arange (0, 512, 1)
	qs = PDWave.query.first() #read first record from the table
	yrange={qs.data}
	results = list(map(int, str(yrange)[2:-2].split(",")))
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
@main.route("/map")
@login_required
def showmap():
	return render_template('map.html')
@main.route("/chat")
@login_required
def chat():
	return render_template('chat.html', room=1)

@main.route('/pdv/api/v1.0/get_prpd', methods=['GET'])
def get_prpd():
	data = {}
	#Phase chart
	t = np.arange (0, 2000, 1)
	data['pdchart_label'] = t.tolist();
	s = 512*np.sin(2*np.pi*(t/2000))
	s = [round(x) for x in s]
	data['pdchart_data'] = s;
	
	datax = []
	datay = []
	pdchart_data = []
	phaseDots=PDWave.query.all()
	for phaseDot in phaseDots:
#phase: 100MHZ/50HZ=2,000,000/1024=1953.1
		datax.append(phaseDot.phase)
		datay.append(phaseDot.peak)
	data['pdchart_plotx'] = datax
	data['pdchart_ploty'] = datay
	return responseJSON(data)
@main.route('/pdv/api/v1.0/get_waveform', methods=['GET'])
def get_waveform():
	selected=0
	if 'selected' in request.args:
		selected = int(request.args['selected'])
	data = {}
	#Waveform
	print("selected:"+str(selected))
	if(int(selected)>0):
		qs = PDWave.query.filter_by(id=selected).first()	
	if(selected<1 or qs is None):
		qs = PDWave.query.first()
	yrange={qs.data}
	results = str(yrange)[2:-2].split(",")
	data['wvchart_data'] = results
	length =len(results)
	print(length)
	xrange = np.arange (0, length, 1)
	data['wvchart_label'] = xrange.tolist()
	#FFT chart
	w = np.fft.fft(list(map(int, results))) #convert to integer first before FFT
	z =np.abs(w[0:int(length/2)]) #FFT result
	data['fftchart_label'] = xrange[0:int(length/2)].tolist()
	data['fftchart_data'] = z.tolist()
	print(data)
	return responseJSON(data)
@main.route('/pdv/api/v1.0/get_fft', methods=['GET'])
def get_fft():
	data = {}
	return responseJSON(data)
@main.route('/pdv/api/v1.0/get_phasepoints', methods=['GET'])
def get_phasepoints():
	selected=0
	if 'selected' in request.args:
		selected = int(request.args['selected'])
	print("selected:"+str(selected))
	qs = PDWave.query.with_entities(PDWave.id,PDWave.upt_time,PDWave.phase,PDWave.peak).filter_by(phase=selected).all()
	print(qs)
	return responseJSON(qs)
def responseJSON(data):
	response = jsonify(data)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
	
#@socketio.on('joined', namespace='/ws')
#def joined(message):
#    print(message)
#    join_room(1)
#    emit('status', {'msg': 'you has entered the room.'}, room=1)
#@socketio.on('text', namespace='/ws')
#def text(message):
#    print(message)
#    emit('message', {'msg': message['msg']}, room=1)
#
#@socketio.on('left', namespace='/ws')
#def left(message):
#    leave_room(1)
#    print("Left the room")
#    emit('status', {'msg': 'You has left the room.'}, room=1)