import requests
import subprocess
from flask import *

#CHANNEL_API_HOST = 'http://localhost:8080'
CHANNEL_API_HOST = 'https://ihome-prod.appspot.com'  # It'd point to version 9
app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';
rpi_id = 'axa-home'


@app.route('/')
def main():
	response = requests.get(CHANNEL_API_HOST + '/issue_channel_api_token/' + rpi_id)
	#print('rrrrrrrr::%s', response.json())

	if response.status_code == 200:
		token = response.json().get('token')
  	return render_template('index.html', rpi_id=rpi_id, token=token)


@app.route("/cgi")
def hello():
    cmd = ["ls", "-l"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out

if __name__ == "__main__":
    app.run()
