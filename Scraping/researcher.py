from elasticsearch_dsl import DocType, String

class Researcher(DocType):
    name = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    tags = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    link = String(index='not_analyzed')

    location = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    institution = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    institution_url = String(index='not_analyzed')

    class Meta:
        index = 'dataforgood'
