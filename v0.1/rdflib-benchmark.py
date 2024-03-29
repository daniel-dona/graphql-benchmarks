#!/usr/bin/env python3
import argparse
import json
import rdflib

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ids_file", required=True, help="Input file with JSON encoded IDs")
parser.add_argument("-o", "--output_timings", required=True, help="Output file with CSV encoded benchmark results")
parser.add_argument("-d", "--debug_querys", required=False, help="Output file with debug data of the run querys")
args = parser.parse_args()

def execute_query(query_path, dataset):
	g = rdflib.Graph()

	print("parsing ...")
	g.parse("./rdflib/"+dataset+".nt", format="nt")

	print("querying ...")
	f = open(query_path, "r")
	query = f.read()
	print("query= " + str(query))

	s = time.time()

	qres = g.query(query)

	delta = time.time() - s

	for row in qres:
		print("%s = " + str(row))



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
				
				if e == "1K":
				
					execute_query(query_path, e)
			
					print(".", end="", flush=True)

					csv += str(e)+","+str(q)+","+str(v_id)+","+str(ms)+"\n"
					
				else:
					
					print("^", end="", flush=True)
			
			print("|", end="", flush=True)
			
		print("]")
		
		


text_file = open(args.output_timings, "w")
text_file.write(csv)
text_file.close()			
		
			


