from researcher import Researcher

import json,os
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

Researcher.init()

path = os.path.realpath('../Scraping/nesetweb/nesetweb')
#path = path + "/members_url_instit_loc_exp.json.try1"

path = path + "/members_url_instit_loc_exp.json"
nameKey = "member"
linkKey = "member_url"
tagsKey = "expertise"

locationKey = "location"
institutionKey = "institution"
institutionUrlKey = "institution_url"

with open(path, 'r') as file:
	    
    content = file.read().decode('utf8')
    #print content
    JsonObjects = json.loads(content)

    count = 0
    for JsonObject in JsonObjects:
        count += 1
        if count % 100 == 0:
            print "{} researchers loaded into ES".format(count)
    	name =  JsonObject[nameKey].encode('utf-8')
    	link =  JsonObject[linkKey].encode('utf-8')
    	tags =  JsonObject[tagsKey]

    	tags = [tag.encode('utf-8') for tag in tags]

        location =  JsonObject[locationKey].encode('utf-8')
        institution =  JsonObject[institutionKey][0].encode('utf-8')
        institution_url =  'https://www.google.fr/search?q="' + institution + '"'


        researcher = Researcher(name=name, tags=tags, link=link, location = location, institution=institution, institution_url=institution_url)
        
        print "researcher :  {}".format(researcher)
        researcher.save()