import pandas as pd

# config twilio
def config ():
	account = "XXXXXX"
	token = "XXXXXX"
	from_tel= 'XXXXXXX'
	path = 'XXXXX.csv'
	return account, token, from_tel, path 

def nom ():
	df = pd.read_csv("nom_numero.csv")
	d = {}
	for i, row in df.iterrows():
		d[str(row['Numero'])] = row['Nom']
	return d 
	

