#!/usr/bin/env python3
import argparse
import json
import tempfile

import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ids_file", required=True, help="Input file with JSON encoded IDs")
parser.add_argument("-o", "--output_timings", required=True, help="Output file with CSV encoded benchmark results")
parser.add_argument("-d", "--debug_querys", required=False, help="Output file with debug data of the run querys")
args = parser.parse_args()

def gen_config(query,port):
	
	mapping = "LinGBM.r2rml.ttl"
	
	run_file = open("tmp/morph.props", "w")
	
	name = run_file.name
	
	output_result_path = tempfile.NamedTemporaryFile()
	
	output = output_result_path.name
	
	props = '''mappingdocument.file.path='''+mapping+'''
	query.file.path='''+query+'''
	output.file.path='''+output+'''

	no_of_database=1
	database.name[0]=benchmark
	database.driver[0]=com.mysql.cj.jdbc.Driver
	database.url[0]=jdbc:mysql://127.0.0.1:'''+port+'''/benchmark?allowPublicKeyRetrieval=true&useSSL=false
	database.user[0]=testing
	database.pwd[0]=1234
	database.type[0]=mysql
	'''
	
	run_file.write(props)
	run_file.close()
	
	return name

def get_port(dataset):
	
	eps = {"1K": '3306', "2K": '3307', "4K": '3308', "8K": '3309', "16K": '3310', }

	return eps[dataset]
	

with open(args.ids_file) as fp:
    ids = json.load(fp)

base_path = "querys"





for q in ids:
	
	for e in ids[q]:
		
		for v_id in ids[q][e]:
			
			query_path = base_path+"/"+str(e)+"/"+str(q)+"/"+str(v_id)+".rq"

			conf = gen_config(query_path,get_port(e))
			
			
			
			print (subprocess.check_output(
				["java", "-cp", ".:morph-rdb/morph-rdb.jar:morph-rdb/lib/*", "es.upm.fi.dia.oeg.morph.r2rml.rdb.engine.MorphRDBRunner", ".", conf],
				stderr=subprocess.STDOUT,
				shell=True))

			print(conf)

			
		
# Descargar directorios con consultas
# Mapear datasets a puertos
# Ejecutar consultas sparql
# Evaluar salida de morph
# Sacar datos para tiempos	
			


