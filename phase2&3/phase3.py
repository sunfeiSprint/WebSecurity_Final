__author__ = 'Sun Fei'

import json
from form import Form
from pprint import pprint


with open('phase1_sample.json') as data_file:
    data = json.load(data_file)


#########check for CSRF####################
for url in data[0]:
    #pprint(url)
   formDetails = data[0][url].pop(0)
   action = formDetails["action"]
   if formDetails["method"] == "get":# form is a get form, it cannot contain a token, always vulnerable for CSRF
        pprint("get form "+formDetails["action"]  +" is vulnerable to CSRF")
        ###try to eliminate non-sensitive-data?###

   elif formDetails["method"] == "post":# form is a post form, check for CSRF
        csrfForm = Form(url,formDetails)
        #First, we send a valid request.
        valid_parameters = dict(csrfForm.fill_entries())
        ####pprint(valid_parameters)
        csrfForm.send(action,valid_parameters,"post")

        # Now, we suppress everything that looks like a token.
        broken_parameters = dict(csrfForm.fill_entries("hidden"))
        content,code = csrfForm.send(action,broken_parameters,"post")
        if code == 200:
            pprint("post form "+csrfForm.formdata["action"] +  " is vulnerable to CSRF")


