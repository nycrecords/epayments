from flask import current_app
from app.models import Suborders
from app import es
from elasticsearch.helpers import bulk
from datetime import datetime
from app.constants.search import DATETIME_FORMAT, ES_DATETIME_FORMAT, RESULTS_CHUNK_SIZE


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
                            "max_gram": 6,
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
                current_app.config["ELASTICSEARCH_INDEX"]: {
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
                        "date_received": {
                            "type": "date",
                            "format": ES_DATETIME_FORMAT,
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
            'date_received': q.order.date_received.strftime(DATETIME_FORMAT),
            'date_submitted': q.order.date_submitted.strftime(DATETIME_FORMAT),
            'billing_name': q.order.customer.billing_name.title(),
            'customer_email': q.order.customer.email,
            'order_type': q.order_type,
            'current_status': q.status,
        })
    num_success, _ = bulk(
        es,
        operations,
        index=current_app.config["ELASTICSEARCH_INDEX"],
        doc_type=current_app.config["ELASTICSEARCH_INDEX"],
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=False
        )
    print("Successfully created %s docs." % num_success)


def update_docs():
    """Updates the elasticsearch index"""
    order = Suborders.query.all()
    for q in order:
        q.es_update()


def delete_doc(suborder_id):
    """Delete a specific doc in the index"""
    es.delete(index=current_app.config['ELASTICSEARCH_INDEX'],
              doc_type=current_app.config["ELASTICSEARCH_INDEX"],
              id=suborder_id)


def search_queries(order_number,
                   suborder_number,
                   order_type,
                   status,
                   billing_name,
                   date_received_start,
                   date_received_end,
                   start, size):
    """Arguments will match search parameters
        :param order_number: search by order number
        :param suborder_number: search by suborder number
        :param order_type:  search by order type
        :param status: search by status
        :param billing_name: search by billing name
        :param date_received_start: search by starting date
        :param date_received_end: search by ending date
        :param start: starting index of the set
        :param size: size of results pool

        :return: elasticsearch results in json format
    """

    # Removes leading and tailing whitespaces
    if order_number is not None:
        order_number = order_number.strip()

    if suborder_number is not None:
        suborder_number = suborder_number.strip()

    if billing_name is not None:
        billing_name = billing_name.strip()

    # Removes 'all' and sets it to nothing: no parameters is all in this case
    if status == 'all':
        status = ''

    if order_type == 'all':
        order_type = ''

    # Time formatting: from mm/dd/yyyy to mm/dd/yy hh:mm AM/PM
    if date_received_start:
        date_received_start = datetime.strptime(date_received_start, '%m/%d/%Y').strftime('%x %I:%M %p')

    if date_received_end:
        date_received_end = datetime.strptime(date_received_end, '%m/%d/%Y').strftime('%x %I:%M %p')

    query_field = {
        'billing_name': billing_name,
        'order_type': order_type,
        'suborder_number': suborder_number,
        'order_number': order_number,
        'current_status': status,
    }

    date_range = {
        'date_received_start': date_received_start,
        'date_received_end': date_received_end
    }

    dsl_gen = DSLGenerator(query_fields=query_field, date_range=date_range)
    dsl = dsl_gen.search() if date_received_start or \
                              billing_name or \
                              date_received_end or \
                              order_type or \
                              suborder_number or \
                              order_number or \
                              status else dsl_gen.no_query()

    # Search query
    search_results = es.search(index=current_app.config["ELASTICSEARCH_INDEX"],
                               doc_type=current_app.config["ELASTICSEARCH_INDEX"],
                               body=dsl,
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
    """Class for generating DSL body for searching"""
    def __init__(self, query_fields, date_range):
        """
        Constructor for class

        :param query_fields: fields to query by
        :param date_range: date range to query by
        """

        self.__query_fields = query_fields
        self.__date_range = date_range

        self.__filters = []

    def search(self):
        """
        Generate dictionary of generic search query
        :return: dictionary with prepended method query
        """

        # Creates dictionary from the fields in __query_fields
        for i in self.__query_fields:
            if self.__query_fields[i]:
                # only search parameter that isn't searched by exact value
                if i is 'billing_name':
                    self.__filters.append({
                        'match': {
                            i: {
                                'query': self.__query_fields[i],
                            }
                        }
                    })
                else:
                    self.__filters.append({
                       'term': {
                           i: self.__query_fields[i]
                       }

                    })

        # Creates dictionary from the fields in date range
        if self.__date_range['date_received_start']:
            if self.__date_range['date_received_end']:
                self.__filters.append({
                    'range': {
                        'date_received': {
                            'gte': self.__date_range['date_received_start'],
                            'lte':  self.__date_range['date_received_end'],
                            'format': ES_DATETIME_FORMAT
                        }
                    }
                })
            else:
                self.__filters.append({
                    'range': {
                        'date_received': {
                            'gte': self.__date_range['date_received_start'],
                            'format': ES_DATETIME_FORMAT
                        }
                    }
                })
        else:
            self.__filters.append({
                'range': {
                    'date_received': {
                        'lte': self.__date_range['date_received_end'],
                        'format': ES_DATETIME_FORMAT
                    }
                }
            })
        return self.__query

    def no_query(self):
        """
        Generates a search query that searches all
        :return: prepended method __must_query
        """
        self.__filters = [
            {'match_all': {}}
        ]
        return self.__must_query

    @property
    def __must_query(self):
        """
        :return: dictionary with key of 'query' and prepended method __must
        """
        return{
            'query': self.__must
        }

    @property
    def __must(self):
        """
        :return: dictionary with key of 'bool' with nested key 'must' and values of method __get_filters
        """
        return{
            'bool': {
                'must': self.__get_filters()
            }
        }

    @property
    def __query(self):
        """
        Dictionary header of DSL body
        :return: nested dictionary
        """
        return{
            'query': {
                'bool': {
                    'must': self.__get_filters()
                },
            }
        }

    def __get_filters(self):
        """
        :return: values from __filters variable
        """
        return self.__filters
