import json
import glob
import unicodedata
import re

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except Exception:#NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def text_to_id(text):
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return text

# Load the csv file containing SNIP values for all journals
data1			 	= open("../data/SNIP_3_years.csv",'r').read().split('\r\n')
data2				= open("../data/journal_docs.csv",'r').read().split('\r\n')
temp_list1			= []
temp_list2			= []
dict1				= {}
dict2				= {}


for record in data1[1:]:
	parts			= record.split(',')
	if parts[1]!='' and parts[2]!='' and parts[3]!='':
		# print(record)
		SNIP_value	= float(parts[1]) + float(parts[2]) + float(parts[3])
		parts[0]	= text_to_id(parts[0])
		temp_list1.append(parts[0])
		dict1[parts[0]] = SNIP_value

for record in data2[1:]:
	parts			= record.split(',')
	if parts[1]!='' and parts[1]!='0':
		# print(record)
		parts[0]	= text_to_id(parts[0])
		temp_list2.append(parts[0])
		dict2[parts[0]] = int(parts[1])


final_list			= []

for name in temp_list1:
	if name in temp_list2:
		final_list.append(name)

temp_list1 = []
temp_list2 = []


Author_DIR		 	= "../Author Data/cnr rao/Papers"
papers				= glob.glob(Author_DIR+"/paper *.json")
count 				= 0

author_snip 		= 0
for paper in papers:
	with open(paper,'r') as infile:
		paper_dict	= json.load(infile)
	publication = paper_dict['publication'].lower()

	for journal in final_list:
		if  publication.startswith(journal+' '):
			# print(journal)
			# print(publication)
			article_SNIP = dict1[journal]/(dict2[journal]*1.0)
			author_snip  += article_SNIP
			count	+= 1
			break
		# if  ' '+journal+' ' in publication:
		# 	print(journal)
		# 	print(publication)
		# 	count	+= 1
		# 	break


print("Number of article matched : "+str(count))
print("Author SNIP value : "+str(author_snip))