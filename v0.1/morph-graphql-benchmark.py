#!/usr/bin/env python3

from graphqlclient import GraphQLClient
import time
import json
from random import randrange
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ids_file", required=True, help="Input file with JSON encoded IDs")
parser.add_argument("-o", "--output_timings", required=True, help="Output file with CSV encoded benchmark results")
parser.add_argument("-d", "--debug_querys", required=False, help="Output file with debug data of the run querys")
args = parser.parse_args()


ep_1K = {"name": '1K', "url": 'http://localhost:4201/graphql'}
ep_2K = {"name": '2K', "url": 'http://localhost:4202/graphql'}
ep_4K = {"name": '4K', "url": 'http://localhost:4204/graphql'}
ep_8K = {"name": '8K', "url": 'http://localhost:4208/graphql'}
ep_16K = {"name": '16K', "url": 'http://localhost:4216/graphql'}


q1 = {'name': 'q1', 'ids_table': 'listOffer', 'query': '''
	query offer_product_review {
	  listOffer(nr: "$$id$$") {
		productWithReviews {
		  reviews {
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
	'''}
	
q2 = {'name': 'q2', 'ids_table': 'listProducer', 'query': '''
	query producer_product_review {
		listProducerWithProduct(nr:"$$id$$") {
    			productWithReviews {
      				reviews { title }
    			}
  		}
	}
	'''}
	
q3 = {'name': 'q3', 'ids_table': 'listReview', 'query': '''
query review_product_producttype_parenttype {
  listReview(nr: "$$id$$") {
    reviewFor {
      producttype {
        nr
        label
        comment
        parent {
          nr
          label
          comment
        }
      }
    }
  }
}
'''}

q4 = {'name': 'q4', 'ids_table': 'listOffer', 'query': '''
query offer_product_review_person_country {
  listOffer(nr: "$$id$$") {
    productWithReviews {
      label
      comment
      reviews {
        title
        text
        rating1
        rating2
        rating3
        rating4
        reviewer {
          country {
            code
          }
        }
      }
    }
  }
}
'''}

q5 = {'name': 'q5', 'ids_table': 'listProductWithReviews', 'query': '''
query product_review_product {
  listProductWithReviews(nr: "$$id$$") {
    reviews {
      title
      reviewFor {
        productWithReviews {
          reviews {
            title
            reviewFor {
              productWithReviews {
                reviews {
                  title
                  reviewFor {
                    product {
                      label
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}	
'''}

q6 = {'name': 'q6', 'ids_table': 'listVendorWithOffers', 'query': '''
query vendor_offer_product_producer_country {
  listVendorWithOffers(nr: "$$id$$") {
    offers {
      product {
        producer {
          country {
            code
          }
        }
      }
    }
  }
}	
'''}

querys = [q1,q2,q3,q4,q5,q6]

#querys = [q6]

endpoints = [ep_1K, ep_2K, ep_4K, ep_8K, ep_16K]

#endpoints = [ep_1K]

with open(args.ids_file, 'r') as fp:
    ids = json.load(fp)
    
#print(ids)
    

information = {}

results = []

csv = ""

csv2 = ""

n_runs = 5

for endpoint in endpoints:

	client = GraphQLClient(endpoint["url"])

	information[endpoint["name"]] = []

	for q in querys:

		print("Running "+str(q["name"])+" on "+str(endpoint["url"])+": [", end="")

		start = time.time()
		
		for v_id in ids[q["name"]][endpoint["name"]]:
			
			v_q = q["query"].replace("$$id$$", str(v_id))

			for i in range(n_runs):

				start_q = time.time()

				results.append({"json": client.execute(v_q), "query": q["name"], "dataset": endpoint["name"], "v_id": v_id})

				delta_q = time.time() - start_q

				csv += str(endpoint["name"])+","+str(q["name"])+","+str(v_id)+","+str(delta_q)+"\n"

				print(".", end="", flush=True)

			print("|", end="", flush=True)


			delta = time.time() - start

			information[endpoint["name"]].append({"query":q["name"], "runtime": (delta/n_runs)})

		print("]")


if args.debug_querys:
	with open(args.output_timings, 'w') as fp:
		json.dump(results, fp)

text_file = open(args.output_timings, "w")
text_file.write(csv)
text_file.close()

