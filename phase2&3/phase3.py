__author__ = 'Sun Fei'

import json
import requests
import parameter
import config
from loginform import fill_login_form
from form import Form
from pprint import pprint

negKeywords = config.negKeywords

def checkStringContainKey(testString,keyWords):
    for word in negKeywords:

        if word in testString:
            return True   
    return False

#pprint(checkStringContainKey(testString,negKeywords))

with open('phase1_final.json') as data_file:
    data = json.load(data_file)


    client = requests.Session()
    start_urls = parameter.login_urls
    login_user = parameter.username
    login_pass = parameter.password

    response = client.get(start_urls[0],verify=False)
    args, url, method = fill_login_form(response.url, response.content, login_user, login_pass)

    loginResponse = client.post(url, data=args, headers=dict(Referer=start_urls))
    pprint(loginResponse)
    jsonform = []
    if "ERROR: Invalid username" in response.content:
        pprint("Login failed")
    else: 
        pprint("login successful")

        for url in data[0]:
            formDetails = data[0][url]
            action = formDetails["action"]
            if checkStringContainKey(action,negKeywords)==False:#check the Negative keywords to filter out non-sensitive data
                if formDetails["method"].lower() == "get":# form is a get form, it cannot contain a token, always vulnerable for CSRF
                    ''#pprint("get form "+formDetails["action"]  +" is vulnerable to CSRF")
                    ###try to eliminate non-sensitive-data?###

                elif formDetails["method"].lower() == "post":# form is a post form, check for CSRF
                    csrfForm = Form(url,formDetails)
                    #First, we send a valid request.
                    valid_parameters = dict(csrfForm.fill_entries())
                    ##pprint(valid_parameters)
                    r = client.post(action,valid_parameters)

                    # Now, we suppress everything that looks like a token.
                    broken_parameters = dict(csrfForm.fill_entries("hidden"))
                    r = client.post(action,broken_parameters)
                    #content,code = csrfForm.send(action,broken_parameters,"post")
                    if r.status_code == 200:
                        formDetails["url"] = url 
                        jsonform.append(formDetails)
                        #pprint("post form "+csrfForm.formdata["action"] +  " is vulnerable to CSRF")

with open("phase3.json",'w') as outfile:
    json.dump(jsonform,outfile,indent=4)
