from app.models import MarriageCertificate
from app import es
from app.constants.search import RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_marriage_cert_index():
    es.indices.create(
        index='marriage_cert',
        body={
            "mappings": {
                'marriage_cert': {
                    "properties": {
                        'suborder_number': {
                            'type': "keyword"
                        }
                    }
                }
            }
        }
    )


def create_marriage_cert_docs():
    if not es:
        return
    marriage_cert = MarriageCertificate.query.all()

    operations = []

    for q in marriage_cert:
        operations.append({
            '_op_type': 'create',
            '_id': q.suborder_number,
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
        index='marriage_cert',
        doc_type='marriage_cert',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s marriage certificates docs." % num_success)
