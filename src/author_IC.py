from subprocess import call
call(["brew","services","start","tor"])
import socks
import socket
socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
socket.socket 								= socks.socksocket

import requests
import urllib.request
from bs4 import BeautifulSoup
import json
import re
import os
import unicodedata
import time
from time import sleep
from random import choice

# Libraries required to limit the time taken by a request
import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass


@contextmanager
def time_limit(seconds):
	def signal_handler(signum, frame):
		raise TimeoutException
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(seconds)
	try:
		yield
	finally:
		signal.alarm(0)

baseurl 									= "https://scholar.google.com"
request_count 								= 0
global_request_count						= 0
DOS_flag									= 0
continous_block_number						= 0

# Checking existenc of the required directory 
def ckdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return


def get_new_soup(aurl):
	global request_count
	global global_request_count
	global DOS_flag
	global continous_block_number

	if DOS_flag == 1:

		call(["brew","services","stop","tor"])
		continous_block_number				+= 1
		if continous_block_number%15==0 and continous_block_number>1:
			print('The last 15 ips have face DOS with the first request.')
			print('Sleeping for 2 mins. Sleep time : '+str(time.asctime(time.localtime(time.time()))))
			sleep(120)
			continous_block_number 			= 0

		call(["brew","services","start","tor"])
		sleep(5)
		while True:
			try: 
				# Waiting 60 seconds to recieve a responser object
				with time_limit(60):
					print(requests.get("http://icanhazip.com").text)
				break
			except Exception:
				print("Error requesting for ip address.")
				continue
		DOS_flag 							= 0

	else:
		continous_block_number 				= 0

	request_count 							+= 1
	global_request_count 					+= 1
	print('Sending a request. Count : '+str(request_count))
	print('Global successful request count : '+str(global_request_count))

	user_agents 							= ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36','Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11','Opera/9.25 (Windows NT 5.1; U; en)','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)','Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1']
	user_agent 								= choice(user_agents)
	hdr 									= {'User-Agent':user_agent}

	while  True:
		try:
			try:
				with time_limit(300):
					content 				= requests.get(aurl,headers=hdr).content
				break
			except TimeoutException:
				print('Request times out. Trying again...')
				continue
		except Exception as err:
			print('Error in request. Error :')
			print(err.message)
			continue

	soup 									= BeautifulSoup(content,'html.parser')
	return soup


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    text = re.sub('_',' ',text)
    return text



def initialize():
    global country_list
    global city_list
    global city_country_dict

    temp_list = open("../data/all_countries.txt","r").read().split('\n')
    country_list = [ text_to_id(i.split('|')[1]) for i in temp_list]

    with open('../data/Continents_Countries.json','r') as infile:
        temp_dict = json.load(infile)

    for continent in temp_dict.keys():
        for country in temp_dict[continent]:
            for city in temp_dict[continent][country]['cities']:
                city = text_to_id(city)
                city_list.append(city)
                city_country_dict[city] = country


def get_user_link(aname):
	global DOS_flag

	searchName 								= re.sub(' ','+',aname)
	# search_link = baseurl + 'scholar?q=author:"'+searchName+'"&btnG=&hl=en&as_sdt=0%2C5'
	author_search_link						= baseurl + '/citations?view_op=search_authors&mauthors=author:"'+searchName+'"&hl=en&oi=ao'
	while True:
		try:
			soup 							= get_new_soup(author_search_link)
			content							=  soup.find('div',{'id':'gs_ccl'})
			try:
				author 						= content.find_all('div',{'class':'gsc_1usr gs_scl'})[0]

			except IndexError:
				return None
			break
		except AttributeError:
			print('Requesting for user link again.')
			DOS_flag 						= 1
	author_page_link 						= baseurl + author.find('h3',{'class':'gsc_1usr_name'}).find('a')['href']
	return author_page_link


def get_user_info(link):
	global DOS_flag

	soup = get_new_soup(link)
	info = soup.find('div',{'id':'gsc_prf_i'})
	required_info = info.findAll('div',{'class':'gsc_prf_il'})
	text = ''
	for line in required_info:
		text += ' '+line.get_text()

	print(text)
	return text

def get_user_country(text):
	global country_list
	global city_list
	global city_country_dict

	text = text_to_id(text)

	for country in country_list:
		if country in text:
			print('mapped in country list')
			return country

	for city in city_list:
		if ' '+city+' ' in text:
			print('City found : '+city)
			return city_country_dict[city]
		if ','+city+' ' in text:
			print('City found : '+city)
			return city_country_dict[city]
		if ' '+city+'.' in text:
			print('City found : '+city)
			return city_country_dict[city]
		if ' '+city+',' in text:
			print('City found : '+city)
			return city_country_dict[city]
		if ','+city+',' in text:
			print('City found : '+city)
			return city_country_dict[city]

	return None


city_list = []
city_country_dict = {}
country_list = []

initialize()
outfile 	= open('../Author Data/cnr rao/Stats/coauthor_country.csv','w')
with open('../Author Data/cnr rao/Stats/CoAuthors.csv','r') as infile:
	records 		= infile.read().split('\n')
	for record in records[2440:]:
		author_name = record.split(',')[0]
		link 		= get_user_link(author_name)
		if not link:
			print('No account found for : '+author_name)
		else:
			info 		= get_user_info(link)
			country		= get_user_country(info)
			print(author_name+','+str(country))
			outfile.write(author_name+','+str(country)+'\n')

call(["brew","services","stop","tor"])