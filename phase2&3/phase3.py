__author__ = 'Sun Fei'

import json
import requests
import parameter
from loginform import fill_login_form
from form import Form
from pprint import pprint


with open('phase1_sample.json') as data_file:
    data = json.load(data_file)


client = requests.session()

start_urls = parameter.login_urls
login_user = parameter.username
login_pass = parameter.password

response = client.get(start_urls)
args, url, method = fill_login_form(response.url, response.body, login_user, login_pass)
loginResponse = client.post(url, data=args, headers=dict(Referer=start_urls))

if "ERROR: Invalid username" in response.body:
    pprint("Login failed")
else: #login successful
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
            r = client.post(action,valid_parameters)

            # Now, we suppress everything that looks like a token.
            broken_parameters = dict(csrfForm.fill_entries("hidden"))
            #content,code = csrfForm.send(action,broken_parameters,"post")
            if r.status_code == 200:
                pprint("post form "+csrfForm.formdata["action"] +  " is vulnerable to CSRF")


