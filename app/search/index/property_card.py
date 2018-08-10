from app.models import PropertyCard
from app import es
from app.constants.search import RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_property_card_index():
    es.indices.create(
        index='property_card',
        body={
            "mappings": {
                'property_card': {
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


def create_property_card_docs():
    if not es:
        return
    property_card = PropertyCard.query.all()

    operations = []

    for q in property_card:
        operations.append({
            '_op_type': 'create',
            '_id': q.id,
            'id': q.id,
            "borough": q.borough,
            "block": q.block,
            "lot": q.lot,
            "building_number": q.building_number,
            "street": q.street,
            "description": q.description,
            "certified": q.certified,
            "mail": q.mail,
            "contact_info": q.contact_info,
            'suborder_number': q.suborder_number
        })

    num_success, _ = bulk(
        es,
        operations,
        index='property_card',
        doc_type='property_card',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s property card docs." % num_success)