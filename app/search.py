from flask import current_app
from app.models import Suborders
from app import es
from elasticsearch.helpers import bulk

def recreate():
    """Deletes then recreates the index"""
    es.indices.delete(current_app.config["ELASTICSEARCH_INDEX"],
                      ignore=[400, 404])
    create_index()
    create_docs()

def create_index():
    """
    Create elasticsearch index with mappings for stories docs.
    """
    es.indices.create(
        index=current_app.config["ELASTICSEARCH_INDEX"],
        body={
            "settings": {
                "analysis": {
                    "tokenizer": {
                        "ngram_tokenizer": {
                            "type": "ngram",
                            "min_gram": 1,
                            "max_gram": 20
                        }
                    },
                    "analyzer": {
                        "ngram_tokenizer_analyzer": {
                            "type": "custom",
                            "tokenizer": "ngram_tokenizer",
                            "filter": [
                                "lowercase"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "suborders": {
                    "properties": {
                        "billing_name": {
                            "type": "text",
                            "analyzer": "ngram_tokenizer_analyzer",
                            "fields": {
                                "exact": {
                                    "type": "text",
                                    "analyzer": "standard",
                                },
                            },
                        },
                        "customer_email": {
                            "type": "text",
                            "analyzer": "ngram_tokenizer_analyzer",
                            "fields": {
                                "exact": {
                                    "type": "text",
                                    "analyzer": "standard",
                                },
                            },
                        },
                        "suborder_number":{
                            "type": 'text',
                            "analyzer": "ngram_tokenizer_analyzer",
                        },
                        "order_type": {
                            "type": "keyword"
                        },
                        "date_created": {
                            "type": "date",
                            "format": "strict_date_hour_minute_second",
                        }
                    }
                }
            }
        }
    )


def create_docs():
    """Creates elasticsearch request docs for every request"""
    if not es:
        return
    orders = Suborders.query.all()

    operations = []

    for q in orders:
        operations.append({
            '_op_type': 'create',
            '_id': q.id,
            'id': q.id,
            'billing_name' : q.order.customer.billing_name,
            'customer_email': q.order.customer.email,
        })
    num_success, _ = bulk(
        es,
        operations,
        index='suborders',
        doc_type='suborders',
        chunk_size=50,
        raise_on_error=False
        )
"""
#scrapped kept in for refrence
def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)
"""


def update_docs():
    """Updates the elasticsearch index"""
    order = Suborders.query.all()
    for q in order:
        q.es_update()


def remove_doc(index, model):
    if not current_app.elasticsearch:
        return
    es.delete(index=index, doc_type=index, id=model.id)

#Hard-coding in sub orders for a 'proof of concept'
#def search_queries(index,query,page,per_page):


def search_queries(query, start, size):
    """Arguments will match search results

        :param query: what the search terms will be
        :param start: starting index of the set
        :param size: size of results pool

        :return: results in json format
    """

    # removes leading and tailing whitespaces
    if query is not None:
        query = query.strip()

    match_type = 'multi_match'

    query_field = {
        'billing_name': True,
        'billing_name.exact': False,
        'customer_email': True,
        'customer_email.exact': True,
        'order_type': True,
        'order_number': True
    }

    dsl_gen = DSLGenerator(query=query, query_fields = query_field, match_type=match_type)
    dsl = dsl_gen.search() if query else dsl_gen.no_query()

    if not current_app.elasticsearch:
        return [], 0
    search_results = es.search(index='suborders',
                               doc_type='suborders',
                               body=dsl,
                               _source=[
                                   'billing_name',
                                   'customer_email',
                                   'order_type',
                                   'suborder_number'
                               ],
                               size=size,
                               from_=start,
                               )
    print(type(search_results))
    return search_results



class DSLGenerator(object):
    """Class for generating DSL for searching"""
    def __init__(self, query, query_fields, match_type):
        """
        Constructor for class

        :param query: string to query for
        :param query_fields: fields to query by
        #:param tags: tags to query by
        :param match_type: type of query
        """
        self.__query = query
        self.__query_fields = query_fields
        self.__match_type = match_type

        #self.__default_filters = [{'terms': {'tag': tags}}]
        self.__filters = []
        self.__conditions = []

    def search(self):
        """GEnerate dictionary of generic search query"""
        self.__filters = [
            {self.__match_type: {
                'query': self.__query,
                'fields': [name for name in self.__query_fields.keys()],
                'type': "most_fields"
            }}
        ]
        self.__conditions.append(self.__must)
        return self.__should

    def no_query(self):
        self.__filters = [
            {'match_all': {}}
        ]
        return self.__must_query

    @property
    def __must_query(self):
        return{
            'query': self.__must
        }

    @property
    def __must(self):
        return{
            'bool': {
                'must': self.__get_filters()
            }
        }

    @property
    def __should(self):
        return{
            'query': {
                'bool': {
                    'should': self.__conditions
                }
            }
        }

    def __get_filters(self):
        return self.__filters
