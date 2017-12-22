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
	liste_num = ['+33XXXXX','+33XXXXX']
	try:
		df = pd.read_csv(path)
		for numero in list_num:
			df = df[df.tel != numero]
	except:
		d = {'tel': [], 'rep1':[], 'rep2': [], 'conversation': []}
		df = pd.DataFrame(d)
		df.to_csv(path, index=False)
	
	# liste des numeros pour sollicitation irc
	envoie_sms(liste_num)

	return Response("Crédit Agricole Chatbot en place :)"), 200

@app.route("/twilio", methods=["POST"])
def traitement():
	response = save_rep()
	return Response(str(response), mimetype="application/xml"), 200

if __name__ == "__main__":
    app.run(debug=True)
