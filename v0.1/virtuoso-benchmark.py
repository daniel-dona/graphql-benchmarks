#!/usr/bin/env python3
import argparse
import json
import time
from SPARQLWrapper import SPARQLWrapper

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ids_file", required=True, help="Input file with JSON encoded IDs")
parser.add_argument("-o", "--output_timings", required=True, help="Output file with CSV encoded benchmark results")
parser.add_argument("-d", "--debug_querys", required=False, help="Output file with debug data of the run querys")
args = parser.parse_args()

def execute_query(query_path, dataset):
	sparql = SPARQLWrapper("http://127.0.0.1/sparql")
	
	f = open(query_path, "r")
	query = f.read()

	sparql.addDefaultGraph("http://"+dataset+".lingbm.morphgraphql.oeg-upm.net/")
	sparql.setQuery(query)
	
	s = time.time()
	
	d = sparql.query()

	delta = time.time() - s
	
	print(d.convert())

	return delta
	
	


with open(args.ids_file) as fp:
	ids = json.load(fp)

base_path = "querys"

n_runs = 5

csv = ""


for q in ids:
	
	print("Running query "+str(q)+": ")
	
	for e in ids[q]:
		
		print(" > "+str(e)+": [", end="")
		
		for v_id in ids[q][e]:
			
			query_path = base_path+"/"+str(e)+"/"+str(q)+"/"+str(v_id)+".rq"

			for i in range(n_runs):
				
				
				
				ms = execute_query(query_path, e)
			
				print(".", end="", flush=True)

				csv += str(e)+","+str(q)+","+str(v_id)+","+str(ms)+"\n"
					

			print("|", end="", flush=True)
			
		print("]")
		
		


text_file = open(args.output_timings, "w")
text_file.write(csv)
text_file.close()			
		
			


