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


ep_1K = {"name": '1K', "url": 'http://localhost:4201/graphql'}
ep_2K = {"name": '2K', "url": 'http://localhost:4202/graphql'}
ep_4K = {"name": '4K', "url": 'http://localhost:4204/graphql'}
ep_8K = {"name": '8K', "url": 'http://localhost:4208/graphql'}
ep_16K = {"name": '16K', "url": 'http://localhost:4216/graphql'}




q1 = {'name': 'q1', 'ids_table': 'listOffer', 'query': '''
	query offer_product_review {
	  listOffer(nr: "$$id$$") {
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
	'''}
	
q2 = {'name': 'q2', 'ids_table': 'listProducer', 'query': '''
	query producer_product_review {
	  listReview {
		title
		products {
		  producer(nr: "$$id$$") {
			nr
		  }
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
          identifier
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
        identifier
        title
        text
        rating1
        rating2
        rating3
        rating4
        reviewer {
          identifier
          country {
            identifier
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
            identifier
            nr
            title
            reviewFor {
              identifier
              product {
                identifier
                nr
                label
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

endpoints = [ep_1K, ep_2K, ep_4K, ep_8K, ep_16K]


def generate_query_ids(querys, endpoints):

	json_david = {}

	for q in querys:

		json_david[q["name"]] = {}

		for e in endpoints:

			ids = random_ids(q["ids_table"],20,e["url"])

			json_david[q["name"]][e["name"]] = ids


	return json_david
	


json = generate_query_ids(querys, endpoints)

print(json)

f = open("data.json", "w")
f.write(json.dumps(json))
f.close()

