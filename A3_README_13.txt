===GROUP 13

-Scanner VM’s MD5 checksum:
(You can use the 'md5sum' Unix utility to compute this. Example: $ md5sum A3-20.vdi)
-Scanner’s VM admin credentials:
-Benchmark VM’s MD5 checksum:
-Benchmark VM’s admin credentials:


===Other ready
(If there is anything we should know before we run your scanner, please let us know here)

The vulnerability category our group deal with is CSRF.

phase 1:

phase 2:

phase 3:

phase 4:
For phase 4, we have worked out two versions of the generation scripts under directory 'phase4':
'generate_exploit.py' and 'generate_exploit_check_response.py'.

Our idea is that we can check the HTML response status code to verify whether the CSRF attack is successful or not. If the response status code is 200, the cross site request is successfully made which means the site is vulnerable to CSRF attack. If the status code is not 200, the request failed which means the site is protected with some other mechanism (like private token etc) and not vulnerable to CSRF attack. The script 'generate_expoit_check_response.py' is used to generate such exploit scripts.

However, during our trial and testing, we did find that due to some implementation issue of the web applications, they still return with response status code 200 even thought the CSRF attack is not successful. Hence, we cannot assume 200 means the web app is vulnerable. The 'generate_exploit.py' script will execute the attack and just leave the browser open to let user inspect the result manually to verify whether the attack is successful or not.

The input of phase 4 is the output of phase 2 & 3, which is the file <file name> retrieved from <file dir>.

Both of the two scritps 'generate_exploit.py' and 'generate_exploit_check_response.py' take 3 arguments. To run either one, just use the following command (use one as example, same way to run the other):
generate_exploit.py -c <config file path> -i <input file> -o <output dir>
- config file path: required, the configuration file, mostly in config dir
- input file: required, input file of phase 4, generated from previous phases
- output dir: optional, the output dir of exploit scriipts, default is user phase4/out
