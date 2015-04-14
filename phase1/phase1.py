import os
from bs4 import BeautifulSoup
import json

formsfile=open('formslist','r')
formsstr=formsfile.read()
formsfile.close()
bfforms=BeautifulSoup(formsstr)
forms=list(set(bfforms.find_all('form')))
jsonform=dict([])
for form in forms:
	formaction=form.get('action')
	formmethod=form.get('method')
	formtype=form.get('type')
	if formtype=='search':
		continue
	formdict=dict([])
	formdict['method']=formmethod
	for inputitem in form.find_all('input'):
		formdict[inputitem.get('name')]=inputitem.get('type')
	jsonform[formaction]=formdict

print jsonform
with open("phase1.json",'w') as outfile:
	json.dump([jsonform],outfile,indent=4)
