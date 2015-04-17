import os
from bs4 import BeautifulSoup
import json
from crawler.spiders import parameter

formsfile=open('formslist','r')
formsstr=formsfile.read()
formsfile.close()
os.remove('formslist')
linksfile=open('linkslist','r')
linksstr=linksfile.read()
linksfile.close()
os.remove('linkslist')
links=linksstr.split('\n')
bfforms=BeautifulSoup(formsstr)
forms=bfforms.find_all('form')
linkforms=zip(links,forms)
linkforms=list(set(linkforms))
jsonform=dict([])
for linkform in linkforms:
	url=linkform[0]
	formaction=linkform[1].get('action')
	formmethod=linkform[1].get('method')
	formtype=linkform[1].get('type')
	if formtype=='search':
		continue
	formdict=dict([])
	formdict['method']=formmethod
	formdict['action']=''.join(parameter.domain)+formaction
	parameterdict=dict([])
	for inputitem in linkform[1].find_all('input'):
		parameterdict[inputitem.get('name')]=inputitem.get('type')
	formdict['parameter']=parameterdict
	jsonform[url]=formdict

#print jsonform
with open("phase1.json",'w') as outfile:
	json.dump([jsonform],outfile,indent=4)
