# main.py
import numpy as np
import re
from .models import PhaseDots
from .models import WaveForm
from . import db
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.name)
	
@main.route("/chart")
@login_required
def chart():
	t = np.arange (0.0, 2000.0, 10.0)
	s = 512*np.sin(2*np.pi*(t/2000.0))
	t = [round(x) for x in t]
	s = [round(x) for x in s]
	phase = []
	amplitude = []
	legend = 'PDChart'
	phaseDots=PhaseDots.query.all()

	for phaseDot in phaseDots:
		phase.append(phaseDot.phase)
		amplitude.append({'x': phaseDot.phase, 'y': phaseDot.peak})
	##print(amplitude)
	ugly_blob = str(amplitude).replace('\'', '')
	#print('ugly_blob')
	#print(ugly_blob)
	return render_template('chart.html', values=ugly_blob, labels=s, phases=t,legend=legend)
	
@main.route("/waveform")
@login_required
def waveform():
	xrange = np.arange (0, 512, 1)
	qs = WaveForm.query.first()
	yrange={qs.data}
	ugly_blob = str(yrange).replace("'", "")
	ugly_blob1= re.sub("[{]","[",ugly_blob)
	ugly_blob2= re.sub("[}]","]",ugly_blob1)
	print(ugly_blob2)
	return render_template('waveform.html', values=ugly_blob2, labels=xrange,legend='WaveForm')
	
@main.route("/fftchart")
@login_required
def fftchart():
	xrange = np.arange (0, 512, 1)
	qs = WaveForm.query.first()
	yrange={qs.data}
	ugly_blob = str(yrange).replace("'", "")
	ugly_blob1= re.sub("[{]","[",ugly_blob)
	ugly_blob2= re.sub("[}]","]",ugly_blob1)
	print(ugly_blob2)
	return render_template('waveform.html', values=ugly_blob2, labels=xrange,legend='FFTChart')