from app.models import Orders
from app import es
from app.constants.search import ES_DATETIME_FORMAT, DATETIME_FORMAT, RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_order_docs():
    if not es:
        return
    orders = Orders.query.all()

    operations = []

    for q in orders:
        operations.append({
            '_op_type': 'create',
            '_id': q.id,
            'order_number': q.id,
            'client_date': q.client_data,
            'multiple_items': q.multiple_items
        })

    num_success, _ = bulk(
        es,
        operations,
        index='orders',
        doc_type='orders',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s order docs." % num_success)