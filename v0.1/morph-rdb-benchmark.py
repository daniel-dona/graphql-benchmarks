#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ids_file", required=True, help="Input file with JSON encoded IDs")
parser.add_argument("-o", "--output_timings", required=True, help="Output file with CSV encoded benchmark results")
parser.add_argument("-d", "--debug_querys", required=False, help="Output file with debug data of the run querys")
args = parser.parse_args()

with open('ids.json') as json_file:
    ids = json.load(json_file)

for q in ids:
	
	for e in q:
		
		for v_id in e:
			
			print(q,e,v_id)
			
			

props = '''mappingdocument.file.path='''+path_mapping+'''example1-mapping-mysql.ttl
query.file.path='''+path_query+'''example1-query01.rq
output.file.path='''+path_output+'''example1-query01-result-mysql.xml

no_of_database=1
database.name[0]=benchmark
database.driver[0]=com.mysql.cj.jdbc.Driver
database.url[0]=jdbc:mysql://mysql-morph:'''+port_server+'''/morph_example?allowPublicKeyRetrieval=true&useSSL=false
database.user[0]=testing
database.pwd[0]=1234
database.type[0]=mysql'''
