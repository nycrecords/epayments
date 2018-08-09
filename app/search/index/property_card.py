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
                        'image_id': {
                            'type': 'text'
                        }

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
            'certificate_number': q.certificate_number,
            'groom_last_name': q.groom_last_name,
            'groom_first_name': q.groom_first_name,
            'bride_last_name': q.bride_last_name,
            'bride_first_name': q.bride_first_name,
            'num_copies': q.num_copies,
            'month': q.month,
            'day': q.day,
            'years': q.years if q.years is not None else "",
            'marriage_place': q.marriage_place,
            'borough': q.borough if q.borough is not None else "",
            'letter': q.letter,
            'comment': q.comment,
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
    print("Successfully created %s marriage search docs." % num_success)