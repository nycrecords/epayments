from app.models import TaxPhoto
from app import es
from app.constants.search import RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_tax_photo_index():
    es.indices.create(
        index='tax_photo',
        body={
            "mappings": {
                'tax_photo': {
                    "properties": {
                        'id': {
                            'type': "keyword"
                        },
                        'suborder_number': {
                            'type': "keyword"
                        },

                    }
                }
            }
        }
    )


def create_tax_photo_docs():
    if not es:
        return
    tax_photo = TaxPhoto.query.all()

    operations = []

    for q in tax_photo:
        operations.append({
            '_op_type': 'create',
            '_id': q.id,
            'id': q.id,
            'borough': q.borough,
            'collection': q.collection,
            'roll': q.roll,
            'block': q.block,
            'lot': q.lot,
            'building_number': q.building_number,
            'street': q.street,
            'description': q.description,
            'size': q.size,
            'num_copies': q.num_copies,
            'mail': q.mail,
            'contact_number': q.contact_number,
            'suborder_number': q.suborder_number,
        })

    num_success, _ = bulk(
        es,
        operations,
        index='tax_photo',
        doc_type='tax_photo',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s tax photo docs." % num_success)
