__author__ = 'Sun Fei'

import requests

class Form(object):
    def __init__(self,url,formdata):
        self.url = url
        self.formdata = formdata
        self.type_dictionary = {"text": "abcdefgh",
                                "email": "ex@amp.le",
                                "password": "abcd1234",
                                "checkbox": "true",
                                "radio": "1",
                                "datetime": "1990-12-31T23:59:60Z",
                                "datetime-local":
                                "1985-04-12T23:20:50.52",
                                "date": "1996-12-19",
                                "month": "1996-12",
                                "time": "13:37:00",
                                "week": "1996-W16",
                                "number": "123456",
                                "range": "1.23",
                                "url": "http://localhost/",
                                "search": "query",
                                "tel": "012345678",
                                "color": "#FFFFFF",
                                "hidden": "Secret.",
                                "submit": "",
                                "name":"abcasdfa",
                                "file":"asdfaf"}

    def fill_entries(self,filter_type=None):
        action = self.formdata["action"]
        method = self.formdata["method"].lower()
        if method =="post":
            params = self.formdata["parameter"]
            for name in params.keys():
                if name != "null":
                    type = params[name]
                    if filter_type is None:
                        if type != "":
                            if type.startswith("hidden_*_"):
                                print(type)
                                splitString= type.split("_*_")
                                value = splitString[1]
                            elif type in self.type_dictionary.keys():
                                value = self.type_dictionary[type]
                            else:
                                value =''
                        yield name, value
                    elif filter_type == "hidden":
                        if type != "" and type !="hidden":
                            if type.startswith("hidden_*_"):
                                splitString= type.split("_*_")
                                value = splitString[1]
                            elif type in self.type_dictionary.keys():
                                value = self.type_dictionary[type]
                            else:
                                value =''
                            yield name, value

    def send(self,url,data,method):
        if method == "get":
            response = requests.get(url, params=data)
        else:
            response = requests.post(url,data=data)
        return response.content,response.code

    def guess_value(self,type,name):
        value = self.type_dictionary.get(type, '')
        supposed_value = self._get_attrib_value("value")

        if supposed_value:
            next_value = supposed_value
        else:
            next_value = value

        if self.get_type == "text":
            if self.maxlength < len(next_value) and not self.maxlength == 0:
                next_value = value[:self.maxlength]

            if self.minlength > len(next_value) and not self.minlength == 0:
                if len(next_value) != 0:
                    required = len(next_value) - self.minlength \
                        / len(next_value)
                    next_value = value.join(value[0] * int(required))

        return next_value
