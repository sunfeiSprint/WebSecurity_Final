__author__ = 'Sun Fei'

import json;


payload = {"text": "abcdefgh",
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
                                "submit": ""}

with open("../output/phase2_output.json", "w") as outfile:
    json.dump({'payloads':payload}, outfile, indent=2)
