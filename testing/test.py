from graphqlclient import GraphQLClient
import time
import json
from random import randrange

def random_ids(table,n,endpoint):

	client = GraphQLClient(endpoint)

	get_max_id = '''query {
	  '''+str(table)+'''{ 
		  nr
	  }
	}'''

	data = json.loads(client.execute(get_max_id))
	max = int(data["data"][table][len(data["data"][table])-1]["nr"])
	ids = []

	for i in range(n):
		ids.append(randrange(max))
	return ids


n_runs = 5

endpoints = ['http://localhost:4201/graphql',
			'http://localhost:4202/graphql',
			'http://localhost:4204/graphql',
			'http://localhost:4208/graphql',
			'http://localhost:4216/graphql']

information = {}

csv = ""

print(random_id("listOffer", 10, endpoints[0]))

quit()
