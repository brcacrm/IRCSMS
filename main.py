from flask import Flask, Response
from twilio import twiml
import pandas as pd

from utils import *
from config import config

_,_,path=config()

app = Flask(__name__)

@app.route("/")
def check_app():
    # returns a simple string stating the app is working
	try:
		df = pd.read_csv(path)	
	except:
		d = {'tel': [], 'rep':[]}
		df = pd.DataFrame(d)
		df.to_csv(path, index=False)
	
	# liste des numeros pour sollicitation irc
	envoie_sms(['+33611967370'])#,'+33676569915'])#,'+33613993802'])

	return Response("Crédit Agricole Chatbot en place :)"), 200

@app.route("/twilio", methods=["POST"])
def traitement():
	response = save_rep()
	return Response(str(response), mimetype="application/xml"), 200

if __name__ == "__main__":
    app.run(debug=True)
