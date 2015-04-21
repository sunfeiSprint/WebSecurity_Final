import os
from bs4 import BeautifulSoup
import json
from crawler.spiders import parameter

try:
	formsfile=open('formslist','r')
except:
	print 'No form!'
	exit()
formsstr=formsfile.read()
formsfile.close()
#os.remove('formslist')
linksfile=open('linkslist','r')
linksstr=linksfile.read()
linksfile.close()
#os.remove('linkslist')
links=linksstr.split('\n')
bfforms=BeautifulSoup(formsstr)
forms=bfforms.find_all('form')
linkforms=zip(links,forms)
linkforms=list(set(linkforms))
jsonform=[]
for linkform in linkforms:
	url=linkform[0]
	formaction=linkform[1].get('action')
	formmethod=linkform[1].get('method')
	formtype=linkform[1].get('type')
	formdict=dict([])
	formdict['url']=url
	formdict['method']=formmethod
	formdict['action']=parameter.domain[0]+'/'+str(formaction)
	parameterdict=dict([])
	for inputitem in linkform[1].find_all('input'):
		#print inputitem
		parameterdict[inputitem.get('name')]=inputitem.get('type')
	formdict['parameter']=parameterdict
	jsonform.append(formdict)
	#print formdict

#print jsonform
with open("phase1.json",'w') as outfile:
	json.dump(jsonform,outfile,indent=4)
