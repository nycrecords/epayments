from flask import current_app
from app.models import Suborders
from app import es
from datetime import datetime
from app.constants.search import DATETIME_FORMAT, ES_DATETIME_FORMAT, RESULTS_CHUNK_SIZE
from app.search.index import (create_suborder_index, create_suborder_docs,
                              create_order_docs, create_orders_index)


def recreate():
    """Deletes then recreates the index"""
    es.indices.delete('*', ignore=[400, 404])
    create_index()
    create_docs()


def create_index():
    """Creates indices """
    create_suborder_index()
    create_orders_index()


def create_docs():
    """Creates elasticsearch request docs for every request"""
    create_suborder_docs()
    create_order_docs()


def delete_doc(suborder_id):
    """Delete a specific doc in the index"""
    es.delete(index=current_app.config['ELASTICSEARCH_INDEX'],
              doc_type=current_app.config["ELASTICSEARCH_INDEX"],
              id=suborder_id)


def search_queries(order_number=None,
                   suborder_number=None,
                   order_type='',
                   status='',
                   billing_name=None,
                   date_received_start='',
                   date_received_end='',
                   date_submitted_start='',
                   date_submitted_end='',
                   start=0,
                   size=RESULTS_CHUNK_SIZE,
                   search_type='search'):
    """Arguments will match search parameters
        :param order_number: search by order number
        :param suborder_number: search by suborder number
        :param order_type:  search by order type
        :param status: search by status
        :param billing_name: search by billing name
        :param date_received_start: search by starting date
        :param date_received_end: search by ending date
        :param date_submitted_start: search by starting date submitted
        :param date_submitted_end: search by ending date submitted
        :param start: starting index of the set
        :param size: size of results pool
        :param search_type: search or print

        :return: elasticsearch results in json format
    """
    query_field = {
        'billing_name': billing_name,
        'order_type': order_type,
        'suborder_number': suborder_number,
        'order_number': order_number,
        'current_status': status,
    }

    date_range = {
        'date_received_start': date_received_start,
        'date_received_end': date_received_end,
        'date_submitted_start': date_submitted_start,
        'date_submitted_end': date_submitted_end
    }

    dsl_gen = DSLGenerator(query_fields=format_queries(query_field), date_range=format_date_range(date_range))
    dsl = dsl_gen.no_query()

    if any(query_field.values()) or any(date_range.values()):
        dsl = dsl_gen.search()

    # Search query
    if search_type == 'search':
        search_results = es.search(index='suborders',
                                   doc_type='suborders',
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
    elif search_type == 'print':
        search_results = es.search(index='suborders',
                                   doc_type='suborders',
                                   body=dsl,
                                   _source=[
                                       'suborder_number',
                                       'order_type',
                                   ],
                                   size=size,
                                   from_=start,
                                   )
        return search_results


def format_queries(query_fields):
    # Removes leading and tailing whitespaces
    if query_fields['order_number'] is not None:
        query_fields['order_number'] = query_fields['order_number'].strip()

    if query_fields["suborder_number"] is not None:
        query_fields["suborder_number"] = query_fields["suborder_number"].strip()

    if query_fields['billing_name'] is not None:
        query_fields['billing_name'] = query_fields['billing_name'].strip()

    # Removes 'all' and sets it to nothing: no parameters is all in this case
    if query_fields['current_status'] == 'all':
        query_fields['current_status'] = ''

    if query_fields['order_type'] == 'all':
        query_fields['order_type'] = ''

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

    def __get_filters(self):
        """
        :return: values from __filters variable
        """
        return self.__filters
