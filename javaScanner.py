import requests as req
from bs4 import BeautifulSoup as bs
import os
import sys
import subprocess
import optparse
from urllib.parse import urljoin


#print('[+] Welcome to the Scanner')
#print('coded By ')


amass_path = '/snap/bin/amass'

def get_argument():

	parser=optparse.OptionParser()
	parser.add_option("-d","--domain",dest="domain",help="Add a Domain")
	(options,arguments) = parser.parse_args()


	if not options.domain:
		parser.error("\n[-] Specify a Domain to scan --help for more details")


	return options



options = get_argument()

na = ['https://' , 'http://']
for a in na:
	if a in options.domain:
		print('Not allowed! Put the domain name as example.com')
		sys.exit()



#Enumerating Subdomains using amass

outfile = options.domain + ".txt"

domains = options.domain + "2.txt"

jsfile = options.domain + "js.txt"


def amass(domain_name):

	if not os.path.exists(amass_path):
		print('[-] subdomain enumeration failed amass not found')
		print('[-] skipping ....')
		return options.domain

	else:

		print("[+] Scanning for the SubDomains...")
		FNULL = open(os.devnull, 'w')
		subprocess.call(["amass", "enum","--passive", "-d", options.domain, "-o", outfile], stdout=FNULL, stderr=subprocess.STDOUT)
		print('[+] Output saved in' + outfile)

	return(outfile)
#checking for valid subdomain
def subdomain_checker():

	print('[+] checking for the subdomain is valid or not')

	if not os.path.exists(outfile):
		print('[-] no subdomain for checking')

	else:
		subdomains2 = open(outfile)
		lines = subdomains2.readlines()

		
		for line in lines:
			resp = req.get('http://'+ line)
			if resp.status_code == 200:
				open(domains, "a+")
				write(line)
			else:
				print('The current subdomain does not exists')


		print('Output saved in ' + domains)

	return(domains)		

#js file extractor
def js_extractor():
	session = requests.Session()
	subdomains3 = open(domains)
	lines = subdomains3.readlines()

	for line in lines:
		html = session.get(line).content
		soup = bs(html, "html.parser")

		for script in soup.find_all("script"):
  			if script.attrs.get("src"):
        	# if the tag has the attribute 'src'
				script_url = urljoin(line, script.attrs.get("src"))
       			open(jsfile, "a+")
        		write(script_url)

    return(jsfile)

#checks the js files for any secret.
def secret_checker():

	secret = ['key', 'token', 'username', 'password', 'Key', 'Token', 'database', 'user', 'pass', 'secret']

	secret_file = open(jsfile)
	url  = secret_file.readlines()

	for u in url:
		if resp.status_code == 200:
			# Make a GET request to fetch the raw HTML content
			html_content = requests.get(u).text

			# Parse the html content
			soup = BeautifulSoup(html_content, "html.parser")
			soup.prettify()

			for s in secret:
				if s in soup:
					print('The File may contain the secrets' + u)

			print('Nothing Found!')

#deleting the created files
def file_delete():

	choice = int(input('would you like to delete the created files: y or n'))

	if (choice == 'y'):

		if os.path.exists(outfile):
			os.remove(outfile)
		if os.path.exists(domains):
			os.remove(domains)
		if os.path.exists(jsfile):
			os.remove(jsfile)


	else:
		sys.exit()
		



	print('Files Successfully Deleted')



if __name__ == "__main__":

	#print('[+] Welcome to the Scanner')
	#print('coded By ')

	amass(options.domain)
	subdomain_checker()
	js_extractor()
	secret_checker()
	file_delete()









