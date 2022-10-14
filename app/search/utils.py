from datetime import datetime

from elasticsearch.helpers import bulk
from flask import current_app
from sqlalchemy.orm import joinedload

from app import es
from app.constants import order_type
from app.constants.search import DATETIME_FORMAT, ES_DATETIME_FORMAT, RESULTS_CHUNK_SIZE
from app.models import (
    BirthSearch,
    BirthCertificate,
    DeathSearch,
    DeathCertificate,
    Hvr,
    MarriageSearch,
    MarriageCertificate,
    NoAmends,
    OCME,
    Orders,
    PhotoGallery,
    Suborders,
    TaxPhoto,
    PropertyCard
)
from app.search.searchfunctions import SearchFunctions


def recreate():
    """Deletes then recreates the index"""
    es.indices.delete(index='suborders', ignore=[400, 404])
    create_index()
    create_docs()


def create_index():
    """Creates indices """
    es.indices.create(
        index='suborders',
        body={
            "settings": {
                "index": {
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
                        },
                    },
                    "max_ngram_diff": 3
                }
            },
            "mappings": {
                "properties": {
                    "customer.billing_name": {
                        "type": "text",
                        "analyzer": "ngram_tokenizer_analyzer",
                        "fields": {
                            "exact": {
                                "type": "text",
                                "analyzer": "standard",
                            },
                        },
                    },
                    "suborder_number": {
                        "type": 'keyword',
                    },
                    "order_number": {
                        "type": 'keyword',
                    },
                    "order_type": {
                        "type": 'keyword',
                    },
                    "current_status": {
                        "type": 'keyword'
                    },
                    "date_received": {
                        "type": "date",
                        "format": ES_DATETIME_FORMAT,
                    },
                    "date_submitted": {
                        "type": "date",
                        "format": ES_DATETIME_FORMAT,
                    },
                    "multiple_items": {
                        "type": "boolean"
                    }
                }
            }
        }
    )


def create_docs():
    """Creates elasticsearch request docs for every request"""
    if not es:
        return
    suborders = Suborders.query.options(joinedload(Suborders.order)).options(
        joinedload(Suborders.order).joinedload(Orders.customer)).all()

    order_type_models_handler = {
        order_types.BIRTH_SEARCH: BirthSearch,
        order_types.BIRTH_CERT: BirthCertificate,
        order_types.MARRIAGE_SEARCH: MarriageSearch,
        order_types.MARRIAGE_CERT: MarriageCertificate,
        order_types.DEATH_SEARCH: DeathSearch,
        order_types.DEATH_CERT: DeathCertificate,
        order_types.NO_AMENDS: NoAmends,
        order_types.TAX_PHOTO: TaxPhoto,
        order_types.PHOTO_GALLERY: PhotoGallery,
        order_types.PROPERTY_CARD: PropertyCard,
        order_types.HVR: Hvr,
        order_types.OCME: OCME,
    }

    operations = []

    for q in suborders:
        try:
            customer = q.order.customer

            operations.append({
                '_op_type': 'create',
                '_id': q.id,
                'order_number': q.order_number,
                'suborder_number': q.id,
                'date_received': q.order.date_received.strftime(DATETIME_FORMAT),
                'date_submitted': q.order.date_submitted.strftime(DATETIME_FORMAT),
                'customer': {
                    'address': customer.address,
                    'billing_name': customer.billing_name.title(),
                    'shipping_name': customer.shipping_name.title(),
                    'address_line_one': customer.address_line_1,
                    'address_line_two': customer.address_line_2,
                    'city': customer.city,
                    'state': customer.state,
                    'zip_code': customer.zip_code,
                    'country': customer.country,
                    'email': customer.email,
                    'phone': customer.phone
                },
                'order_type': q.order_type,
                'current_status': q.status,
                'metadata': order_type_models_handler[q.order_type].query.filter_by(
                    suborder_number=q.id).one().serialize,
                'multiple_items': q.order.multiple_items,
                'order_types': q.order.order_types
            })
        except:
            pass

    num_success, _ = bulk(
        es,
        operations,
        index='suborders',
        chunk_size=1000,
        raise_on_error=True
    )
    print("Successfully created %s suborder docs." % num_success)


def delete_doc(suborder_id):
    """Delete a specific doc in the index"""
    es.delete(index=current_app.config['ELASTICSEARCH_INDEX'],
              id=suborder_id)


def search_queries(order_number=None,
                   suborder_number=None,
                   order_type='all',
                   delivery_method='',
                   status='',
                   billing_name=None,
                   email=None,
                   date_received_start='',
                   date_received_end='',
                   date_submitted_start='',
                   date_submitted_end='',
                   multiple_items='',
                   start=0,
                   size=RESULTS_CHUNK_SIZE,
                   search_type='search'):
    """Arguments will match search parameters
        :param order_number: search by order number
        :param suborder_number: search by suborder number
        :param order_type: search by order type
        :param delivery_method: search by delivery method
        :param status: search by status
        :param billing_name: search by billing name
        :param email: search by email
        :param date_received_start: search by starting date
        :param date_received_end: search by ending date
        :param date_submitted_start: search by starting date submitted
        :param date_submitted_end: search by ending date submitted
        :param multiple_items: search by multiple items in cart
        :param start: starting index of the set
        :param size: size of results pool
        :param search_type: search or print

        :return: elasticsearch results in json format
    """
    query_field = {
        'billing_name': billing_name,
        'suborder_number': suborder_number,
        'order_number': order_number,
        'current_status': status,
        'multiple_items': multiple_items,
        'metadata.delivery_method': delivery_method,
        'email': email
    }

    date_range = {
        'date_received_start': date_received_start,
        'date_received_end': date_received_end,
        'date_submitted_start': date_submitted_start,
        'date_submitted_end': date_submitted_end,
    }

    formatted_date_range = format_date_range(date_range)

    dsl_gen = DSLGenerator(query_fields=format_queries(query_field),
                           date_range=formatted_date_range,
                           order_type=format_order_type(order_type),
                           search_type=search_type)
    dsl = dsl_gen.match_all()

    if any(query_field.values()) or any(date_range.values()):
        dsl = dsl_gen.search()

    # Search query
    search = SearchFunctions()

    return search.search_by(search_type, dsl, start, size)


def format_queries(query_fields):
    # Removes leading and tailing whitespaces
    if query_fields['order_number'] is not None:
        query_fields['order_number'] = query_fields['order_number'].strip()

    if query_fields['suborder_number'] is not None:
        query_fields['suborder_number'] = query_fields['suborder_number'].strip()

    if query_fields['billing_name'] is not None:
        query_fields['billing_name'] = query_fields['billing_name'].strip()

    if query_fields['email'] is not None:
        query_fields['email'] = query_fields['email'].strip()

    # Removes 'all' and sets it to nothing: no parameters is all in this case
    if query_fields['current_status'] == 'all':
        query_fields['current_status'] = ''

    if query_fields['metadata.delivery_method'] == 'all':
        query_fields['metadata.delivery_method'] = ''

    return query_fields


def format_date_range(date_range):
    # Remove 'Invalid date' as an option
    # Time formatting: from mm/dd/yyyy to mm/dd/yy hh:mm AM/PM
    for a in date_range:
        if date_range[a] == 'Invalid date':
            date_range[a] = ''
        if date_range[a]:
            date_range[a] = datetime.strptime(date_range[a], '%m/%d/%Y').strftime(DATETIME_FORMAT)

    return date_range


def format_order_type(order_type):
    if order_type == 'all':
        return None
    elif order_type == 'vital_records':
        return order_types.VITAL_RECORDS_LIST
    elif order_type == 'photos':
        return order_types.PHOTOS_LIST
    else:
        return [order_type]


class DSLGenerator(object):
    """Class for generating DSL body for searching"""

    def __init__(self, query_fields, date_range, order_type, search_type):
        """
        Constructor for class

        :param query_fields: fields to query by
        :param date_range: date range to query by
        """

        self.__query_fields = query_fields
        self.__date_range = date_range
        self.__search_type = search_type

        self.__default_filters = [{'terms': {'order_type': order_type}}] if order_type else []
        self.__filters = []
        self.__sort_filters = []

    def search(self):
        """
        Generate dictionary of generic search query
        :return: dictionary with prepended method query
        """
        # Creates dictionary from the fields in __query_fields
        for i in self.__query_fields:
            if self.__query_fields[i]:
                # only search parameter that isn't searched by exact value
                if i == 'billing_name':
                    self.__filters.append({
                        'match': {
                            "customer.billing_name": {
                                'query': self.__query_fields[i],
                                'operator': 'and'
                            }
                        }
                    })
                elif i == 'email':
                    self.__filters.append({
                        'match': {
                            'customer.email': {
                                'query': self.__query_fields[i],
                                'operator': 'and'
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
        date_ranges = {}

        # Initializes the keys 'date received' and 'date submitted' and sets it with a dict
        if self.__date_range['date_received_start'] or self.__date_range['date_received_end']:
            date_ranges['date_received'] = {'format': ES_DATETIME_FORMAT}

        if self.__date_range['date_submitted_start'] or self.__date_range['date_submitted_end']:
            date_ranges['date_submitted'] = {'format': ES_DATETIME_FORMAT}

        # Sets the nested keys 'gte' and 'lte' based on whats given
        if self.__date_range['date_received_start']:
            date_ranges['date_received']['gte'] = self.__date_range['date_received_start']

        if self.__date_range['date_received_end']:
            date_ranges['date_received']['lte'] = self.__date_range['date_received_end']

        if self.__date_range['date_submitted_start']:
            date_ranges['date_submitted']['gte'] = self.__date_range['date_submitted_start']

        if self.__date_range['date_submitted_end']:
            date_ranges['date_submitted']['lte'] = self.__date_range['date_submitted_end']

        # Appends the filters with the full range queries
        if self.__date_range['date_received_start'] or self.__date_range['date_received_end']:
            self.__filters.append({
                'range': {
                    'date_received': date_ranges['date_received']}})

        if self.__date_range['date_submitted_start'] or self.__date_range['date_submitted_end']:
            self.__filters.append({
                'range': {
                    'date_submitted': date_ranges['date_submitted']}})

        return self.__query

    def match_all(self):
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
        return {
            'sort': [
                '_score',

                {'date_received': 'desc'} if self.__query_fields['current_status'] else {'date_received': 'asc'}
                if self.__date_range['date_received_start'] else {'date_received': 'desc'},

                {'date_submitted': 'asc'},
            ],
            'query': self.__must,
            "aggs": {
                "order_count": {
                    "cardinality": {
                        "field": "order_number"
                    }
                }
            }
        }

    @property
    def __must(self):
        """
        :return: dictionary with key of 'bool' with nested key 'must' and values of method __get_filters
        """
        return {
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
        if self.__search_type in ['search', 'print', 'csv']:
            return {
                'sort': [
                    '_score',

                    {'date_received': 'desc'} if self.__query_fields['current_status'] else {'date_received': 'asc'}
                    if self.__date_range['date_received_start'] else {'date_received': 'desc'},

                    {'date_submitted': 'asc'},
                ],
                'query': {
                    'bool': {
                        'must': self.__get_filters()
                    },
                },
                "size": 0,
                "aggs": {
                    "order_count": {
                        "cardinality": {
                            "field": "order_number"
                        }
                    }
                }
            }
        else:
            return {
                'query': {
                    'bool': {
                        'must': self.__get_filters()
                    }
                }
            }

    def __get_filters(self):
        """
        :return: values from __filters variable
        """
        return self.__filters + self.__default_filters
