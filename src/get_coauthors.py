import json
import glob
import re

Author_DIR		 	= "../Author Data/cnr rao/Papers"
papers				= glob.glob(Author_DIR+"/paper *.json")
authors = {}
for paper in papers:
	with open(paper,'r') as infile:
		paper_dict	= json.load(infile)
		for author in paper_dict['authors']:
			author = re.sub('[ ]+$','',author.lower())
			author = re.sub('[ ]+',' ',author)
			if author!= '' and author!='...':
				try:
					authors[author] += 1
				except KeyError:
					authors[author] = 1
final_list = {}
for name in authors:
	if authors[name]>0:
		try:
			final_list[authors[name]].append(name)
		except KeyError:
			final_list[authors[name]] = []
			final_list[authors[name]].append(name)

with open('../Author Data/cnr rao/Stats/CoAuthors.csv','w') as outfile:
	for count in sorted(final_list.keys(),reverse=True):
		for author in final_list[count]:
			parts = author.split(' ')
			author = ''
			for part in parts:
				author += ' '+part[:1].upper() +part[1:]
			outfile.write(author+','+str(count)+'\n')
