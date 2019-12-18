#!/usr/bin/env python3
import argparse
import json
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ids_file", required=True, help="Input file with JSON encoded IDs")
parser.add_argument("-o", "--output_timings", required=True, help="Output file with CSV encoded benchmark results")
parser.add_argument("-d", "--debug_querys", required=False, help="Output file with debug data of the run querys")
args = parser.parse_args()

def gen_config(mapping,query,output,port):
	
	query_file = tempfile.NamedTemporaryFile()
	
	props = '''mappingdocument.file.path='''+mapping+'''example1-mapping-mysql.ttl
	query.file.path='''+query+'''example1-query01.rq
	output.file.path='''+output+'''example1-query01-result-mysql.xml

	no_of_database=1
	database.name[0]=benchmark
	database.driver[0]=com.mysql.cj.jdbc.Driver
	database.url[0]=jdbc:mysql://mysql-morph:'''+port+'''/morph_example?allowPublicKeyRetrieval=true&useSSL=false
	database.user[0]=testing
	database.pwd[0]=1234
	database.type[0]=mysql'''
	
	query_file.write(props)

def get_port(dataset):
	
	eps = {"1K": '3306', "2K": '3307', "4K": '3308', "8K": '3309', "16K": '3310', }

	return eps[dataset]
	

with open(args.ids_file) as fp:
    ids = json.load(fp)

base_path = "querys"

lingbm_mapping = "./LinGBM.r2rml.ttl"

for q in ids:
	
	for e in ids[q]:
		
		for v_id in ids[q][e]:
			
			query_path = base_path+"/"+str(e)+"/"+str(q)+"/"+str(v_id)+".rq"
			
			conf = gen_config(lingbm_mapping,query_path,output_result_path,get_port(e))
		
# Descargar directorios con consultas
# Mapear datasets a puertos
# Ejecutar consultas sparql
# Evaluar salida de morph
# Sacar datos para tiempos	
			


