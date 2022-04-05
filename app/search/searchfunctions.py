from app import es


class SearchFunctions(object):

    def search_by(self, search_type, dsl, start, size):
        order_type_handler = {
            'Birth Search': 'birth_search',
            'Birth Cert': 'birth_cert',
            'Marriage Search': 'marriage_search',
            'Marriage Cert': 'marriage_cert',
            'Death Search': 'death_search',
            'Death Cert': 'death_cert',
            'Tax Photo': 'tax_photo',
            'Photo Gallery': 'photo_gallery',
            'Property Card': 'property_card',
            'print': 'print',
            'search': 'search',
            'customer': 'customers',
            'order': 'orders',
            'csv': 'csv'
        }
        method = getattr(self, order_type_handler[search_type])
        return method(dsl, start, size)

    @staticmethod
    def search(dsl, start, size):
        search_results = es.search(index='suborders',
                                   aggs=dsl["aggs"],
                                   query=dsl["query"],
                                   sort=dsl["sort"],
                                   _source=[
                                       'order_number',
                                       'suborder_number',
                                       'date_received',
                                       'order_type',
                                       'current_status',
                                       'customer'
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    @staticmethod
    def print(dsl, start, size):
        search_results = es.search(index='suborders',
                                   aggs=dsl["aggs"],
                                   query=dsl["query"],
                                   sort=dsl["sort"],
                                   _source=[
                                       'suborder_number',
                                       'order_type',
                                       'order_number',
                                       'date_submitted',
                                       'customer',
                                       'metadata',
                                       'multiple_items',
                                       'order_types'
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    @staticmethod
    def csv(dsl, start, size):
        search_results = es.search(index='suborders',
                                   doc_type='suborders',
                                   scroll='1m',
                                   body=dsl,
                                   _source=[
                                       'order_number',
                                       'suborder_number',
                                       'date_received',
                                       'order_type',
                                       'customer',
                                       'metadata'
                                   ],
                                   size=size,
                                   from_=start)

        sid = search_results['_scroll_id']
        scroll_size = search_results['hits']['total']

        scroll_results = search_results['hits']['hits']

        while scroll_size > 0:
            results = es.scroll(scroll='1m', body={"scroll": "1m", "scroll_id": sid})

            scroll_size = len(results['hits']['hits'])

            scroll_results += results['hits']['hits']

        return scroll_results

    @staticmethod
    def format_results(results):
        results_len = len(results['hits']['hits'])
        return [results['hits']['hits'][i]['_source'] for i in range(results_len)]

    @staticmethod
    def format_first_result(results):
        return results['hits']['hits'][0]['_source']
