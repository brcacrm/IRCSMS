from flask import request
import pandas as pd
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
from config import config
from text2num import text2num, Small

account, token, path = config()

# texte premier sms
def irc_q1 ():
	message_body = 'Bonjour, suite à votre échange avec votre conseiller du Crédit Agricole, nous souhaiterons recueillir votre avis. Quelle note de 0 à 10 donnez-vous à cet échange ? (0 = pas du tout satisfait, 10 = très satisfait)'
	return message_body

# envoie du premier sms
def envoie_sms(to_num):
	body = irc_q1()
	client = Client(account, token)
	for tel in to_num:
		try:
			message = client.messages.create(to=tel, from_="+33757905368",
                                 body=body)
		except:
			verif_telephone_number(client,tel)

# complete et sauvegarde le dataset irc_sms.csv
def save_rep():
	message_body = request.form['Body']
	phone_number = request.form['From']
	write=True
	
	try:
		message_body = int(message_body)
	except:
		message_body = message_body.lower()
		if message_body in Small:
			message_body = text2num(message_body)
		elif message_body == 'chut':
			message_body = -1 #sursollicitation
		else:
			#message auto je n'ai pas compris votre reponse (redemander noter + STOP)
			print('message incompris')
			write = False
			resp = unknow_sms()
	
	if write:	
		df = pd.read_csv(path)
		d = {'tel': [phone_number], 'rep':[message_body]}
		tmp = pd.DataFrame(d)
		df = df.append(tmp)
		df.to_csv(path, index=False)
		
		resp = rep_default()

	return resp

	
# envoyer une reponse automatique de remerciement
def rep_default():
	resp = MessagingResponse()
	resp.message('Le Crédit Agricole Sud Rhône Alpes vous remercie pour votre reponse !')
	return str(resp)

#message incompris
def unknow_sms():
	resp = MessagingResponse()
	resp.message('Nous n\'avons pas compris votre note. Merci de bien vouloir renoter. Quelle note de 0 à 10 donnez-vous à cet échange ? (0 = pas du tout satisfait, 10 = très satisfait) Dite CHUT pour ne plus recevoir de message.')
	return str(resp)

# verification de nouveau numeros
def verif_telephone_number(client,tel):
	validation_request = client.validation_requests.create(tel,friendly_name="")
	print('Call Validation Code new phone number ('+ str(tel) + ') :')
	print('\t'+ str(validation_request.validation_code))
	return str(validation_request.validation_code)
