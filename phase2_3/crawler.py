import requests
import parameter
from pprint import pprint
from bs4 import BeautifulSoup
from loginform import fill_login_form

client = requests.Session()

start_urls = "https://app4.com/"
login_user = parameter.username
login_pass = parameter.password


response = client.get(start_urls,verify=False)


soup = BeautifulSoup(response.content)

pprint (type(soup))

links = soup.findAll("form")

pprint(links)