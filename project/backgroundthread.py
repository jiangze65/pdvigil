# backgroundthread.py
import threading
from flask import Blueprint, render_template,current_app
from . import db
import time
from datetime import datetime
from .models import PDWave

backgroundthread = Blueprint('backgroundthread', __name__)

class StoppableThread (threading.Thread):
    def __init__(self, target, name):
        super (StoppableThread, self).__init__(target = target, name = name)
        self._stop = threading.Event ()
    def run (self):
        firstTime=True
        while not self._stop.is_set ():
            time.sleep (1)
            if firstTime:
                reloadDB()
                fristTime=False
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

@backgroundthread.route('/start')
def start ():
    name = "Acquisition"
    if name:
        if not get_thread_by_name (name):
            th = StoppableThread (target = StoppableThread, name = name)
            th.start ()
            #reloadDB()
    return render_template('index.html')
	
@backgroundthread.route ('/stop')
def stop ():
    name = "Acquisition"
    if name:
        thread = get_thread_by_name (name)
        if thread:
            thread.stop ()
    return render_template('index.html')
def reloadDB():
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
	