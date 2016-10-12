import json
import glob
import re

if __name__ == "__main__":
	base_dir 	= '../Author Data/S Natarajan/Papers'
	papers 		= glob.glob(base_dir+'/paper*.json')

	citation_count = {}
	for paper in papers:
		with open(paper,'r') as infile:
			data = json.load(infile)

		if data["citations"]:
			for citation in data["citations"]:
				for author in citation['authors']:
					name = re.sub('[ ]+$','',author.lower())
					name = re.sub('[ ]+',' ',name)
					if name!= '':
						try:
							citation_count[name] += 1
						except KeyError:
							citation_count[name] = 1

	final_list = {}
	for name in citation_count:
		if citation_count[name]>0:
			try:
				final_list[citation_count[name]].append(name)
			except KeyError:
				final_list[citation_count[name]] = []
				final_list[citation_count[name]].append(name)

	with open('../Author Data/S Natarajan/Stats/citing_authors.csv','w') as outfile:
		for count in sorted(final_list.keys(),reverse=True):
			for author in final_list[count]:
				parts = author.split(' ')
				author = ''
				for part in parts:
					author += ' '+part[:1].upper() +part[1:]
				outfile.write(author+','+str(count)+'\n')
				# print(str(count)+' '+author)
			# print(str(count)+' '+str(final_list[count]))