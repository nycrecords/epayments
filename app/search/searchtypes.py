from app import es


class SearchFunctions(object):

    def search_by(self, search_type, dsl, start, size):
        order_type_handler = {
                "Birth Search": 'birth_search',
                "Birth Cert": 'birth_cert',
                "Marriage Search": 'marriage_search',
                "Marriage Cert": 'marriage_cert',
                "Death Search": 'death_search',
                "Death Cert": 'death_cert',
                "Tax Photo": 'tax_photo',
                "Photo Gallery": 'photo_gallery',
                "Property Card": 'property_card',
                "print": 'print',
                'search': 'search',
                "customer": 'customers',
                'order': 'orders'
                }
        method = getattr(self, order_type_handler[search_type])
        return method(dsl, start, size)

    def search(self, dsl, start, size):
        search_results = es.search(index='suborders',
                                   doc_type='suborders',
                                   body=dsl,
                                   _source=[
                                       'order_number',
                                       'suborder_number',
                                       'date_received',
                                       'billing_name',
                                       'billing_name',
                                       'customer_email',
                                       'order_type',
                                       'current_status',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def print(self, dsl, start, size):
        search_results = es.search(index='suborders',
                                   doc_type='suborders',
                                   body=dsl,
                                   _source=[
                                       'suborder_number',
                                       'order_type',
                                       'order_number'
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def orders(self, dsl, start, size):
        search_results = es.search(index='orders',
                                   doc_type='orders',
                                   body=dsl,
                                   _source=[
                                        'order_number',
                                        'date_submitted',
                                        'date_received',
                                        'confirmation_message',
                                        'order_types',
                                        'client_data',
                                        'multiple_items',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def birth_cert(self, dsl, start, size):
        search_results = es.search(index='birth_cert',
                                   doc_type='birth_cert',
                                   body=dsl,
                                   _source=[
                                       'certificate_number',
                                       'first_name',
                                       'last_name',
                                       'middle_name',
                                       'gender',
                                       'father_name',
                                       'mother_name',
                                       'num_copies',
                                       'month',
                                       'day',
                                       'years',
                                       'birth_place',
                                       'borough',
                                       'letter',
                                       'comment',
                                       'suborder_number'
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def birth_search(self, dsl, start, size):
        search_results = es.search(index='birth_search',
                                   doc_type='birth_search',
                                   body=dsl,
                                   _source=[
                                        'first_name',
                                        'last_name',
                                        'middle_name',
                                        'gender',
                                        'father_name',
                                        'mother_name',
                                        'num_copies',
                                        'month',
                                        'day',
                                        'years',
                                        'birth_place',
                                        'borough',
                                        'letter',
                                        'comment',
                                        'suborder_number',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def customers(self, dsl, start, size):
        search_results = es.search(index='customers',
                                   doc_type='customers',
                                   body=dsl,
                                   _source=[
                                        'billing_name',
                                        'email',
                                        'shipping_name',
                                        'address_line_one',
                                        'address_line_two',
                                        'city',
                                        'state',
                                        'zip_code',
                                        'country',
                                        'phone',
                                        'instructions',
                                        'order_number',
                                        'address',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def death_cert(self, dsl, start, size):
        search_results = es.search(index='death_cert',
                                   doc_type='death_cert',
                                   body=dsl,
                                   _source=[
                                        'certificate_number',
                                        'first_name',
                                        'last_name',
                                        'middle_name',
                                        'num_copies',
                                        'cemetery',
                                        'month',
                                        'day',
                                        'years',
                                        'death_place',
                                        'borough',
                                        'letter',
                                        'comment',
                                        'suborder_number',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def death_search(self, dsl, start, size):
        search_results = es.search(index='death_search',
                                   doc_type='death_search',
                                   body=dsl,
                                   _source=[
                                        'first_name',
                                        'last_name',
                                        'middle_name',
                                        'num_copies',
                                        'cemetery',
                                        'month',
                                        'day',
                                        'years',
                                        'death_place',
                                        'borough',
                                        'letter',
                                        'comment',
                                        'suborder_number',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def marriage_cert(self, dsl, start, size):
        search_results = es.search(index='marriage_cert',
                                   doc_type='marriage_cert',
                                   body=dsl,
                                   _source=[
                                        'certificate_number',
                                        'groom_last_name',
                                        'groom_first_name',
                                        'bride_last_name',
                                        'bride_first_name',
                                        'num_copies',
                                        'month',
                                        'day',
                                        'years',
                                        'marriage_place',
                                        'borough',
                                        'letter',
                                        'comment',
                                        'suborder_number',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def marriage_search(self, dsl, start, size):
        search_results = es.search(index='marriage_search',
                                   doc_type='marriage_search',
                                   body=dsl,
                                   _source=[
                                        'groom_last_name',
                                        'groom_first_name',
                                        'bride_last_name',
                                        'bride_first_name',
                                        'num_copies',
                                        'month',
                                        'day',
                                        'years',
                                        'marriage_place',
                                        'borough',
                                        'letter',
                                        'comment',
                                        'suborder_number',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def tax_photo(self, dsl, start, size):
        search_results = es.search(index='tax_photo',
                                   doc_type='tax_photo',
                                   body=dsl,
                                   _source=[
                                        'borough',
                                        'collection',
                                        'roll',
                                        'block',
                                        'lot',
                                        'building_number',
                                        'street',
                                        'description',
                                        'size',
                                        'num_copies',
                                        'mail',
                                        'contact_number',
                                        'suborder_number',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def photo_gallery(self, dsl, start, size):
        search_results = es.search(index='photo_gallery',
                                   doc_type='photo_gallery',
                                   body=dsl,
                                   _source=[
                                        "image_id",
                                        "description",
                                        "additional_description",
                                        "size",
                                        "num_copies",
                                        "mail",
                                        "contact_number",
                                        "personal_use_agreement",
                                        "comment",
                                        "suborder_number",
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def property_card(self, dsl, start, size):
        search_results = es.search(index='property_card',
                                   doc_type='property_card',
                                   body=dsl,
                                   _source=[
                                        "borough",
                                        "block",
                                        "lot",
                                        "building_number",
                                        "street",
                                        "description",
                                        "certified",
                                        "mail",
                                        "contact_info",
                                        'suborder_number',
                                   ],
                                   size=size,
                                   from_=start)
        return search_results

    def format_results(unformatted_results):
        results_len = len(unformatted_results['hits']['hits'])
        return [unformatted_results['hits']['hits'][i]["_source"] for i in range(results_len)]

    def format_first_result(unformatted_results):
        return unformatted_results['hits']['hits'][0]["_source"]
