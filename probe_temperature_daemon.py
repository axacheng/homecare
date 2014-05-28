#!/usr/bin/python

import json
import requests
import subprocess
import time

from daemon import runner


DS18B20_PATH = '/sys/bus/w1/devices/28-000005b89736'
CMD = """cat %s/w1_slave |grep -o t=.* | cut -d '=' -f 2""" % DS18B20_PATH
URL = 'http://192.168.0.107:8080/_ah/api/homecare/v1/addTemperature'
USER_ID = 'axa'
TIMES = 60  # 1 minute (60 seconds)


class App():
  def __init__(self):
      self.stdin_path = '/dev/null'
      self.stdout_path = '/dev/tty'
      self.stderr_path = '/dev/tty'
      self.pidfile_path =  '/tmp/foo.pid'
      self.pidfile_timeout = 5
  
  def run(self):
    while True:
      temperature = float(subprocess.Popen([CMD],
                          stdout=subprocess.PIPE,
                          shell=True).communicate()[0]) / 1000
      payload = {}
      payload['current_temperature'] = str(temperature)
      payload['user_id'] = USER_ID
      response = requests.post(URL, data=json.dumps(payload))
      print response.text
      time.sleep(TIMES)


app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()





