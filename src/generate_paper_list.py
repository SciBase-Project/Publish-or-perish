import json
import glob

def get_paper_list(author_dir):

	files 						= glob.glob(author_dir+'/Papers/paper*.json')
	paper_list 					= []
	for file in files:
		with open(file,'r') as infile:
			paper_dict				= json.load(infile)
		paper_list.append(paper_dict['title'])
		# print('Paper : '+file)
		# print(paper_dict['title'])

	# print(paper_list)
	return paper_list

def check_self_cites(paper_list,author_dir):

	files 						= glob.glob(author_dir+'/Papers/paper*.json')
	self_cites 					= 0
	total_cites					= 0
	author_count				= 0
	total_self_cites			= 0

	for file in files:
		with open(file,'r') as infile:
			paper_dict			= json.load(infile)

		if paper_dict['citations'] != None:
			total_cites += len(paper_dict['citations'])
			for citation in paper_dict['citations']:
				if citation['Title'] in paper_list:
					self_cites 		+= 1
				else:
					for author in citation['authors']:
						if 'cnr rao' in author.lower():
							author_count+=1
							# print('Paper title : '+str(citation['Title']))
							# print('Author Name :'+str(author))

	print('Total cites : '+str(total_cites))
	# print('Self cites : '+str(self_cites))
	# print('Author cites : '+str(author_count))
	total_self_cites 			= self_cites + author_count
	print('Self cites : '+str(total_self_cites))
	OCQ							= 1 -(total_self_cites/(1.0*total_cites))
	print('OCQ : '+str(OCQ))

if __name__ == "__main__":
	base_dir 					= '../Author Data/cnr rao'
	paper_list 					= get_paper_list(base_dir)
	check_self_cites(paper_list,base_dir)