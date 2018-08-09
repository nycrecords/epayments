from app.models import Customers
from app import es
from app.constants.search import RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_customers_index():
    es.indices.create(
        index='customers',
        body={
            "mappings": {
                'customers': {
                    "properties": {
                        'id': {
                            'type': "keyword"
                        },
                        'order_number': {
                            'type': "keyword"
                        },

                    }
                }
            }
        }
    )


def create_customers_docs():
    if not es:
        return
    customers = Customers.query.all()

    operations = []

    for q in customers:
        operations.append({
            '_op_type': 'create',
            '_id': q.id,
            'billing_name': q.billing_name,
            'email': q.email,
            'shipping_name': q.shipping_name,
            'address_line_one': q.address_line_1,
            'address_line_two': q.address_line_2,
            'city': q.city,
            'state': q.state,
            'zip_code': q.zip_code,
            'country': q.country,
            'phone': q.phone,
            'instructions': q.instructions,
            'order_number': q.order_number,
            'address': q.address
        })

    num_success, _ = bulk(
        es,
        operations,
        index='customers',
        doc_type='customers',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s birth certificate docs." % num_success)