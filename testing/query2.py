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
	'''}
	
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
	
q3 = {'name': 'q3', 'query': '''
query review_product_producttype_parenttype {
  listReview(nr: "8") {
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

q4 = {'name': 'q4', 'query': '''
query offer_product_review_person_country {
  listOffer(nr: "2") {
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

q5 = {'name': 'q5', 'query': '''
query product_review_product {
  listProductWithReviews(nr: "370") {
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

q6 = {'name': 'q6', 'query': '''
query vendor_offer_product_producer_country {
  listVendorWithOffers(nr: "1") {
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

q11 = {'name': 'q11', 'query': '''
query subquerySearch {
  listOffer {
    price
    offerWebpage
    vendor(nr: "1") {
      nr
    }
    product {
      label
      comment
    }
  }
}
'''}

q12 = {'name': 'q12', 'query': '''
query subqueryFilter1 {
  listOffer {
    identifier
    price
    offerWebpage
    vendor(nr: "1") {
      identifier
    }
    product {
      identifier
      label
      comment
      producer(nr: "16") {
        identifier
      }
    }
  }
}	
'''}

querys = [q1,q2,q3,q4,q5,q6,q11,q12]

#querys = [q11]

n_runs = 20

ep_1K = {"name": '1K', "url": 'http://localhost:4201/graphql'}
ep_2K = {"name": '2K', "url": 'http://localhost:4202/graphql'}
ep_4K = {"name": '4K', "url": 'http://localhost:4204/graphql'}
ep_8K = {"name": '8K', "url": 'http://localhost:4208/graphql'}
ep_16K = {"name": '16K', "url": 'http://localhost:4216/graphql'}


endpoints = [ep_1K, ep_2K, ep_4K, ep_8K, ep_16K]

#endpoints = [ep_1K]

information = {}

results = []

csv = ""

csv2 = ""

for endpoint in endpoints:

	client = GraphQLClient(endpoint["url"])

	information[endpoint["name"]] = []

	for q in querys:

		print("Running "+str(q["name"])+" on "+str(endpoint["url"])+": [", end="")

		start = time.time()

		for i in range(n_runs):

			start_q = time.time()

			results.append(client.execute(q["query"]))

			delta_q = time.time() - start_q

			csv += str(endpoint["name"])+","+str(q["name"])+","+str(delta_q)+"\n"

			print(".", end="", flush=True)

		print("]")

		delta = time.time() - start

		information[endpoint["name"]].append({"query":q["name"], "runtime": (delta/n_runs)})

		csv2 += str(endpoint["name"])+","+str(q["name"])+","+str(delta/n_runs)+"\n"

print(information)
#print(results)

text_file = open("full_report.csv", "w")
text_file.write(csv)
text_file.close()

text_file = open("summary_report.csv", "w")
text_file.write(csv2)
text_file.close()

#text_file = open("data.json", "w")
#text_file.write(results)
#text_file.close()

