import os
from bs4 import BeautifulSoup
import json
from crawler.spiders import parameter

def isin(formdict,jsonform):
	for i in jsonform:
		if formdict['action'] != i['action'] or formdict['parameter'] != i['parameter']:
			continue
		else:
			return True
	return False




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
	if formmethod==None:
		formmethod='get'
	formdict['method']=formmethod
	#print url
	#print formaction
	if str(formaction).find("http") < 0:
		if len(str(formaction))>0 and str(formaction)[0]=='#':
			if  (len(str(formaction))>1 and str(formaction)[1]=='/') or len(str(formaction))==1:
				formdict['action']=url+str(formaction)[1:]
			else:
				if url[-1:]!='/':
					formdict['action']=url+'/'+str(formaction)[1:]
				else:
					formdict['action']=url+str(formaction)[1:]
		else:
			if (len(str(formaction))>0 and str(formaction)[0]!='/') or len(str(formaction))==0:
				direct=url.split('/')
				path=''
				for i in range(len(direct)-1):
					path=path+direct[i]+'/'
				formdict['action']=path+str(formaction)
			else:
				formdict['action']=parameter.domain[0]+str(formaction)
	else:
		formdict['action']=str(formaction)

	parameterdict=dict([])
	for inputitem in linkform[1].find_all('input'):
		#print inputitem
		if inputitem.get('type')=='hidden':
			if inputitem.get('value') is not None:
				parameterdict[inputitem.get('name')]=inputitem.get('type')+'_*_'+inputitem.get('value')
			else:
				parameterdict[inputitem.get('name')]=inputitem.get('type')+'_*_'+''
		else:
			parameterdict[inputitem.get('name')]=inputitem.get('type')
	formdict['parameter']=parameterdict
	if isin(formdict,jsonform):
			continue
	else:
		jsonform.append(formdict)
	#print formdict

#print jsonform
with open("../output/phase1_output.json",'w') as outfile:
	json.dump(jsonform,outfile,indent=4)


