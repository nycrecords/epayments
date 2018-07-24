from flask import current_app
from app.models import Suborders
from app import es
from elasticsearch.helpers import bulk
from datetime import datetime

#constants
ELASTICSEARCH_DATETIME = '%m/%d/%Y'



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
                            "min_gram": 3,
                            "max_gram": 5,
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
                        "suborder_number":{
                            "type": 'keyword',
                        },
                        "order_number": {
                            "type": 'keyword',
                        },
                        "order_type": {
                            "type": 'keyword',
                            "similarity":'boolean'
                        },
                        "current_status": {
                            "type": 'keyword'
                        },
                        "date_created": {
                            "type": "date",
                            "format": "MM/dd/yyyy",
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
            'order_number': q.order_number,
            'suborder_number': q.id,
            'date_received': q.order.date_received.strftime(ELASTICSEARCH_DATETIME),
            'date_submitted': q.order.date_submitted.strftime(ELASTICSEARCH_DATETIME),
            'billing_name': q.order.customer.billing_name,
            'customer_email': q.order.customer.email,
            'order_type': q.order_type,
            'current_status': q.status,
        })
    num_success, _ = bulk(
        es,
        operations,
        index='suborders',
        doc_type='suborders',
        chunk_size=200,
        raise_on_error=False
        )
    print("Successfully created %s docs." % num_success)


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


def search_queries(order_number,
                   suborder_number,
                   order_type,
                   status,
                   billing_name,
                   date_received_start,
                   date_received_end,
                   start, size):
    """Arguments will match search results

        :param query: what the search terms will be
        :param start: starting index of the set
        :param size: size of results pool

        :return: results in json format
    """

    # removes leading and tailing whitespaces
    if order_number is not None:
        order_number = order_number.strip()

    if suborder_number is not None:
        suborder_number = suborder_number.strip()

    if billing_name is not None:
        billing_name = billing_name.strip()

    if status == 'all':
        status = ''

    if order_type == 'all':
        order_type = ''

    match_type = 'match'

    query_field = {
        'billing_name': billing_name,
        'order_type': order_type,
        'suborder_number': suborder_number,
        'order_number': order_number,
        'current_status': status,
    }

    date_range = [
        {'range': {
            'date_received':{
                'gte': date_received_start,
                'lte': date_received_end if date_received_end else date_received_start,
                'format': "MM/dd/yyyy"
            }
        }}
    ]



    dsl_gen = DSLGenerator( query_fields = query_field, date_range= date_range ,match_type=match_type)
    dsl = dsl_gen.search() if date_received_start else dsl_gen.no_query()

    if not current_app.elasticsearch:
        return [], 0
    search_results = es.search(index='suborders',
                               doc_type='suborders',
                               body= dsl,
                               _source=[
                                   'order_number',
                                   'suborder_number',
                                   'date_received',
                                   'date_submitted',
                                   'billing_name',
                                   'customer_email',
                                   'order_type',
                                   'current_status',
                               ],
                               size=size,
                               from_=start,
                               )
    return search_results



class DSLGenerator(object):
    """Class for generating DSL for searching"""
    def __init__(self,query_fields,date_range , match_type):
        """
        Constructor for class

        :param query_fields: fields to query by
        :param match_type: type of query
        """

        self.__query_fields = query_fields
        self.__match_type = match_type
        self.__date_range = date_range

        self.__filters = []
        self.__conditions = []

    def search(self):
        """GEnerate dictionary of generic search query"""

        for i in self.__query_fields:
            if self.__query_fields[i]:
                if i is 'billing_name':
                    self.__filters.append({
                        'match': {
                            i: {
                                'query': self.__query_fields[i],
                                #'minimum_should_match': '75%'
                            }
                        }
                    })
                else:
                    self.__filters.append({
                       'term': {
                           i: self.__query_fields[i]
                       }

                    })
        self.__conditions.append(self.__get_filters())
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
                    'must': self.__get_filters()
                },
            }
        }

    def __get_filters(self):
        return self.__filters
