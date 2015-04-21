import json,sys
with open(sys.argv[1]) as datafile:
	data=json.load(datafile)
parapy=open('./crawler/spiders/parameter.py','w+')
buf="login_urls=['"+data['login_url']+"']\n"
buf=buf+"start_urls=['"+data['start_url']+"']\n"
buf=buf+"domain=['"+data['domain']+"']\n"
buf=buf+"username='"+data['username']+"'\n"
buf=buf+"password='"+data['password']+"'\n"
buf=buf+"login="+data['login']+"\n"
parapy.write(buf)
parapy.close()