from researcher import Researcher

import json,os
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

Researcher.init()

path = os.path.realpath('../ScrapeResearchGate/scrapy_RG')
path = path + "/members_url_instit_loc_exp.json.try1"

nameKey = "member"
linkKey = "member_url"
tagsKey = "expertise"

with open(path, 'r') as file:
	    
    content = file.read().decode('utf8')
    #print content
    JsonObjects = json.loads(content)


    for JsonObject in JsonObjects:
    	name =  JsonObject[nameKey].encode('utf-8')
    	link =  JsonObject[linkKey].encode('utf-8')
    	tags =  JsonObject[tagsKey]

    	tags = [tag.encode('utf-8') for tag in tags]
        researcher = Researcher(name=name, tags=tags, link=link)
        researcher.save()