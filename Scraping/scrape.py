

from urllib2 import urlopen
import bs4 as BeautifulSoup
import pprint
import re


from elasticsearch import Elasticsearch
es = Elasticsearch()

#print soup.prettify()

data_research = {}

tagsKey = "tags"
nameKey = "name"
linkKey = "link"

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

	url = "http://www.dauphine.fr/fr/personnels/enseignants/cvtri/" + letter +  ".html"
	print "Scraping url ", url


	html = urlopen(url)
	soup = BeautifulSoup.BeautifulSoup(html)


	for item in soup.findAll("div", attrs = {"class" : "dauphinecv-item"}):
		str_name = item.h2.text.strip()
		#print str_name

		researcherObject = data_research.get(str_name, {})

		taglist = researcherObject.get(tagsKey, [])

		cvlink =  "http://www.dauphine.fr/" + item.find("a", attrs={"href":re.compile("fr/personnels/enseignants/cv/*")})["href"]




		for ul in item.find_all("ul" ,attrs={"class":"dauphinecv-item-enseignement"}):
			for a in ul.find_all("a"):
				tag =  a.text.strip()
				#print tag
				taglist.append(tag)


		researcherObject[nameKey] = str_name
		researcherObject[linkKey] = cvlink		
		researcherObject[tagsKey] = taglist	
		
		data_research[str_name] = researcherObject
		#print researcherObject	


pprint.pprint(data_research)


from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

from researcher import Researcher

Researcher.init()

for name in data_research:
	researcherObject = data_research[name]
	name = researcherObject[nameKey].encode('utf-8')
	tags = researcherObject[tagsKey]
	tags = [tag.encode('utf-8') for tag in tags]
	link = researcherObject[linkKey].encode('utf-8')

	institution = "Unversite Paris Dauphine".encode('utf-8')
	institution_url = "http://www.dauphine.fr/fr/index.html".encode('utf-8')
	location = "Paris, France".encode('utf-8')

	print name
	print link
	print tags

	
	researcher = Researcher(name=name, tags=tags, link=link, location = location, institution = institution, institution_url=institution_url)
	researcher.save()



print(connections.get_connection().cluster.health())
