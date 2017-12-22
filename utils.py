from flask import request
import pandas as pd
from twilio.rest import Client
from twilio.twiml.messaging_response import Message, MessagingResponse
from config import config, nom
from text2num import text2num, Small

account, token, from_tel, path = config()
dico_num2nom = nom()

# texte premier sms
def irc_q1 ():
	message_body = '\n le Crédit Agricole est engagé dans une démarche d\'amélioration continue. Afin de vous satisfaire et de mieux connaître vos besoins, nous vous proposons de répondre à quelques questions.\n Recommanderiez-vous le Crédit Agricole Sud Rhône Alpes à votre famille, un ami ou un collègue? (0 = non pas du tout, 10 = oui entièrement)'
	return message_body

# texte deuxieme sms (si note<10) 
def irc_q2 ():
	message_body = 'Que devrions-nous faire pour obtenir une note de 10?'
	return message_body

# envoie du premier sms
def envoie_sms(to_num):
	client = Client(account, token)
	for tel in to_num:
		key = tel
		name = dico_num2nom[key[1:]]
		body = '\n Bonjour Monsieur ' + name + ', ' + irc_q1()
		try:
			message = client.messages.create(to=tel, from_=from_tel,
                                 body=body)
		except:
			verif_telephone_number(client,tel)

# complete et sauvegarde le dataset irc_sms.csv
def save_rep():
	message_body = request.form['Body']
	phone_number = request.form['From']
	write=True
	df = pd.read_csv(path)
	
	if all([df.ix[i,'tel']!=int(phone_number) for i in range(df.shape[0])]):
		try:
			message_body = int(message_body)
		except:
			message_body = message_body.lower().strip()
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
			d = {'tel': [phone_number], 'rep1':[message_body], 'rep2': [0], 'conversation': [message_body]}
			tmp = pd.DataFrame(d)
			df = df.append(tmp)
			df.to_csv(path, index=False)

			if message_body < 10 and message_body!=1 :
				body = irc_q2()
				resp = MessagingResponse()
				resp.message(body)
			else:
				resp = rep_default()
	else: 
		df.ix[df['tel']==int(phone_number),'rep2']=message_body
		df.ix[df['tel']==int(phone_number),'conversation'] = str(df.ix[df['tel']==int(phone_number),'conversation'][0]) + '/' + str(message_body)
		df.to_csv(path, index=False)
		resp = rep_default()

	return resp

	
# envoyer une reponse automatique de remerciement
def rep_default():
	resp = MessagingResponse()
	resp.message('Le Crédit Agricole Sud Rhône Alpes vous remercie pour vos réponses !')
	return str(resp)

#message incompris
def unknow_sms():
	resp = MessagingResponse()
	resp.message('Nous n\'avons pas compris votre note. Merci de bien vouloir renoter. Recommanderiez-vous le Crédit Agricole Sud Rhône Alpes à votre famille, un ami ou un collègue? (0 = non pas du tout, 10 = oui entièrement)')
	return str(resp)

# verification de nouveau numeros
def verif_telephone_number(client,tel):
	validation_request = client.validation_requests.create(tel,friendly_name="")
	print('Call Validation Code new phone number ('+ str(tel) + ') :')
	print('\t'+ str(validation_request.validation_code))
	return str(validation_request.validation_code)
