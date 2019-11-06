import csv
import requests
import demjson
import time

post_url = 'https://219wx3mpv4-2.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.27.0%3BJS%20Helper%202.25.1&x-algolia-application-id=219WX3MPV4&x-algolia-api-key=b528008a75dc1c4402bfe0d8db8b3f8e'

header = {'accept':'application/json',
'content-type':'application/x-www-form-urlencoded',
'Origin':'https://www.techinasia.com',
#'Referer':'https://www.techinasia.com/companies?country_name[]=India&country_name[]=China&country_name[]=Australia&country_name[]=Japan&country_name[]=Hong%20Kong&country_name[]=Austria',
'Referer': 'https://www.techinasia.com/companies?country_name[]=China&industry_name[]=Financial%20tech',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

data = {"requests":[{"indexName":"companies","params":"query=&hitsPerPage=10&maxValuesPerFacet=2000&page=7&facets=%5B%22*%22%2C%22entity_locations.country_name%22%2C%22entity_industries.vertical_name%22%2C%22funding_stages.stage_name%22%2C%22employee_count%22%2C%22job_posting_count%22%5D&tagFilters=&facetFilters=%5B%5B%22entity_industries.vertical_name%3AFinancial%20tech%22%5D%5D"},{"indexName":"companies","params":"query=&hitsPerPage=1&maxValuesPerFacet=1000&page=0&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=entity_locations.country_name"}]}
#data = {"requests":[{"indexName":"companies","params":"query=&hitsPerPage=100&maxValuesPerFacet=2000&page=7&facets=%5B%22*%22%2C%22entity_locations.country_name%22%2C%22entity_industries.vertical_name%22%2C%22funding_stages.stage_name%22%2C%22employee_count%22%2C%22job_posting_count%22%5D&tagFilters=&facetFilters=%5B%5B%22entity_locations.country_name%3AIndia%22%2C%22entity_locations.country_name%3AChina%22%2C%22entity_locations.country_name%3AHong%20Kong%22%2C%22entity_locations.country_name%3ASingapore%22%5D%5D"},{"indexName":"companies","params":"query=&hitsPerPage=1&maxValuesPerFacet=1000&page=0&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=entity_locations.country_name"}]}


def get_page(): #get page
    response = demjson.decode(requests.post(post_url, headers=header, data=demjson.encode(data)).text)
    return response.get('results')[-1].get("nbPages")



def get_content():
        for page in range(1,get_page()):
            print(page)
            data = {"requests": [{"indexName": "companies", "params": "query=&hitsPerPage=10&maxValuesPerFacet=2000&page={}&facets=%5B%22*%22%2C%22entity_locations.country_name%22%2C%22entity_industries.vertical_name%22%2C%22funding_stages.stage_name%22%2C%22employee_count%22%2C%22job_posting_count%22%5D&tagFilters=&facetFilters=%5B%5B%22entity_industries.vertical_name%3AFinancial%20tech%22%5D%5D".format(page)}, {"indexName": "companies", "params": "query=&hitsPerPage=1&maxValuesPerFacet=1000&page=0&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=entity_locations.country_name"}]}
            response = requests.post(post_url,headers=header,data=demjson.encode(data))#demjson model to request 
            time.sleep(1)
            #print(response.text)
            if response.status_code == 200: #status code
                resp_json = demjson.decode(response.text)#transfer into json
                data_list = resp_json.get("results")[0].get("hits")
                print(data_list != [])
                if data_list != []:
                    count = 0
                    for item in data_list:#for each company
                    
                        try:
                            count += 1
                            name = item.get("name")
                            entity_locations = item.get("entity_locations")[0]
                            #location = str(entity_locations.get('city_name')) +' ' +str(entity_locations.get("country_name"))#地点
                            country = str(entity_locations.get("country_name"))
                            city = str(entity_locations.get('city_name'))
                            date_founded = str(item.get("date_founded"))
                            entity_industries = item.get("entity_industries")[0]
                            entity_sector = entity_industries.get("vertical_name")
                            entity_area = entity_industries.get("slug")
                            entity_interest = entity_industries.get("name")
                            description = item.get('pitch')
                            employee_count = item.get("employee_count").replace("-", "to")

                            if item.get('funding_stages') != []:
                                funding = item.get('funding_stages')[0]
                                funding_stage = funding.get('stage_name')
                                if funding.get('rounds') != []:
                                    funding_rounds = funding.get('rounds')[0]
                                    funding_amount = funding_rounds.get('amount')
                                    funding_date = funding_rounds.get('date_ended')
                                else:
                                    funding_amount = 0
                                    funding_date = None
                            
                            else:
                                funding_stage = None
                                funding_amount = 0
                                funding_date = None

                            
                            entity_sites = item.get("entity_sites")
            
                            data_list = [(item.get("site_name"),item.get('url')) for item in entity_sites]
                            row = (2,count,name,country,city,data_list,entity_area,entity_interest,description,employee_count,date_founded,funding_stage,funding_amount,funding_date)
                            with open('results.csv', 'a', encoding='gb18030', newline='') as  f:
                                # obtain writer object
                                writer = csv.writer(f)
                                # write into one row
                                writer.writerow(row)
                            print(row)
                        except Exception as e:
                            print(e)
                else:
                    print("No more data!\n The web crawler program terminates!")
                    break
                

if __name__ == '__main__':
    get_content()
