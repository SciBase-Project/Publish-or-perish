file = "../Author Data/cnr rao/Stats/coauthors_with_country.csv"
data = open(file,'r').read()
records = data.split('\n')

national_count = 0
external_count = 0

for record in records:
	country = record.split(',')[1]
	if country.lower() == 'india':
		national_count += 1
	else:
		external_count += 1

print('National co-author count : '+str(national_count))
print('External co-author count : '+str(external_count))

total_count = national_count + external_count
print('Total co-author count : '+str(total_count))

IC = external_count/(1.0*total_count)
print('IC : '+str(IC))