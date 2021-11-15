#!/usr/bin/python3
import yaml
import sys

if(len(sys.argv) < 3):     # just to be sure we have all args 
	print ("please use: ./fstpr.py input.yaml output_fstab")   #and a little help here
	exit()

result = ""                   # defining a string for final results
yaml_file = str(sys.argv[1])  # our input yaml file
fstab_file = str(sys.argv[2]) # output file

with open(yaml_file, 'r') as yf:
	yaml_data = yaml.safe_load(yf)  # reading yaml

ff = open(fstab_file, 'w')          # opening output file

for keys, vals in yaml_data.items():  # walking through yaml data 
	for key, val in vals.items():
		if('root-reserve' in val):    # checking for unsafe options
			rr = str(val['root-reserve']).strip('%')
			print('''WARNING! Unsafe option! Do on unmounted partition only:
"sudo tune2fs -m{} {}"'''.format((rr),key))
		if('export' in val):                 # formatting nfs path
			result = key+':'+val['export']+'\t'+val['mount']
		else:
			result = key+'\t'+val['mount']   # or just regular local partition
		
		result += '\t'+val['type']

		if('options' in val):                # checking for additional options
			result +='\tdefaults'
			for opt in val['options']:
				result += ','+opt
		else:
			result += '\tdefaults'

		if(val['mount'] == '/boot'):         # big volumes of data better not to check on boot
			result += '\t0 2\n'              # but little volumes like boot or root we can check
		elif(val['mount'] == '/'):
			result += '\t0 1\n'
		else:
			result += '\t0 0\n'

		ff.write(result)   # writing finals

ff.close()  # closing open files
yf.close()
