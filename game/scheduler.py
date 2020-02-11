"""HQTrivia schedule

This is where the timely scheduler is implemented.
The jobs for the questions to run can be started and stop from here
"""
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .consumers import GameConsumer
import time
scheduler = BackgroundScheduler()
def start():
    """
    Starts  the scheduler. We call this when the app is started    
    """
    scheduler.start()
def add_new_job(self,roomname,context):
    """
    Initiate a job that  runs to  change the question in different interval

    Args: 
        arg1 (str): name of the room
        arg1 (str): context of the  job
    """
    scheduler.add_job(GameConsumer.check_score, 'interval',args=[self,roomname,context] ,seconds=15,id=roomname)
def stop(roomname):
    """
    Stops a job that is running
    
    Args: 
        arg1 (str): name of the room
    """
    scheduler.remove_job(roomname)