from app.models import Suborders
from app import es
from app.constants.search import ES_DATETIME_FORMAT, DATETIME_FORMAT, RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_suborder_index():
    es.indices.create(
        index='suborders',
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
                'suborders': {
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
                    }
                }
            }
        }
    )


def create_suborder_docs():
    if not es:
        return
    suborders = Suborders.query.all()

    operations = []

    for q in suborders:
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
        index='suborders',
        doc_type='suborders',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s suborder docs." % num_success)

