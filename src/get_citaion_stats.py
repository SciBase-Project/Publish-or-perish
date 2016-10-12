import json
import glob
import re

def get_students_list(author_dir):

	with open('../data/Student_names_format_changed.txt','r') as infile:
		data = infile.read()
		data = re.sub('[.]','',data)
		name_list = []
		temp_name_list = data.split('\n')
		for name in temp_name_list:
			parts = name.split(',')
			new_name = parts[1] + ' ' + parts[0]
			name_list.append(new_name.lower())

		return name_list

def get_paper_list(author_dir):

	files 						= glob.glob(author_dir+'/Papers/paper*.json')
	paper_list 					= []
	for file in files:
		with open(file,'r') as infile:
			paper_dict				= json.load(infile)
		paper_list.append(paper_dict['title'])
	return paper_list

def check_self_cites(paper_list,author_dir,student_names):

	files 						= glob.glob(author_dir+'/Papers/paper*.json')
	self_cites 					= 0
	total_cites					= 0
	student_cites				= 0
	flag						= 0
	flag2						= 0

	for file in files:
		with open(file,'r') as infile:
			paper_dict			= json.load(infile)

		if paper_dict['citations'] != None:
			total_cites += len(paper_dict['citations'])
			for citation in paper_dict['citations']:
				if citation['Title'] in paper_list:
					self_cites 		+= 1
				else:
					flag 		= 0
					for author in citation['authors']:
						if 'cnr rao' in author.lower():
							self_cites+=1
							flag	= 1
					if flag == 0:
						for author in citation['authors']:
							for student in student_names:
								if student == author.lower() or (student+' ') == author.lower():
									student_cites += 1
									flag2 		= 1
									break
							if flag2 == 1:
								flag2 = 0
								break

	print('Total cites : '+str(total_cites))
	print('Self cites : '+str(self_cites))
	OCQ							= 1 -(self_cites/(1.0*total_cites))
	print('OCQ : '+str(OCQ))
	print('Citations from students : '+str(student_cites))

if __name__ == "__main__":
	base_dir 					= '../Author Data/cnr rao'
	student_names = get_students_list(base_dir)
	paper_list 					= get_paper_list(base_dir)
	check_self_cites(paper_list,base_dir,student_names)