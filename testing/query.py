from graphqlclient import GraphQLClient
import time

q1 = {'name': 'q1', 'query': '''
	query offer_product_review {
	  listOffer(nr: "2") {
		identifier
		productWithReviews {
		  identifier
		  reviews {
			identifier
			title
			text
			reviewDate
			publishDate
			rating1
			rating2
		  }
		}
	  }
	}
'''
}

q2 = {'name': 'q2', 'query': '''
	query producer_product_review {
	  listReview {
		title
		products {
		  producer(nr: "8") {
			nr
		  }
		}
	  }
	}
	'''}

#querys = [q1,q2,q3,q4,q5,q6,q11,q12]
querys = [q1,q2]

n_runs = 100

endpoints = ['http://localhost:4201/graphql',
			'http://localhost:4202/graphql',
			'http://localhost:4204/graphql',
			'http://localhost:4208/graphql',
			'http://localhost:4216/graphql']


#endpoints = ['http://localhost:4201/graphql', 'http://localhost:4202/graphql']


information = {}

for endpoint in endpoints:
	
	client = GraphQLClient(endpoint)
	
	information[endpoint] = {}

	for q in querys:
		
		start = time.time()
		
		for i in range(n_runs):
			
			client.execute(q["query"])
			
		delta = time.time() - start
		
		print(q["name"])
		print(delta)

