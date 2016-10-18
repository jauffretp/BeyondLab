

from urllib2 import urlopen
import bs4 as BeautifulSoup
import pprint

from elasticsearch import Elasticsearch
es = Elasticsearch()

#print soup.prettify()

data_research = {}

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

	url = "http://www.dauphine.fr/fr/personnels/enseignants/cvtri/" + letter +  ".html"
	print "Scraping url ", url


	html = urlopen(url)
	soup = BeautifulSoup.BeautifulSoup(html)


	for item in soup.findAll("div", attrs = {"class" : "dauphinecv-item"}):
		str_name = item.h2.text.strip()
		#print str_name
		taglist = data_research.get(str_name, [])


		for ul in item.find_all("ul" ,attrs={"class":"dauphinecv-item-enseignement"}):
			for a in ul.find_all("a"):
				tag =  a.text.strip()
				#print tag
				taglist.append(tag)

		data_research[str_name] = taglist		


pprint.pprint(data_research)


from elasticsearch_dsl import DocType, String
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Researcher(DocType):
    name = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    tags = String(index='not_analyzed')



    class Meta:
        index = 'dataforgood'


Researcher.init()

for name in data_research:
	tags = data_research[name]
	print name
	print tags

	
	researcher = Researcher(name=name, tags=tags)
	researcher.save()



print(connections.get_connection().cluster.health())