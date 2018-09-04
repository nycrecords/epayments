from app.models import DeathCertificate
from app import es
from app.constants.search import RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_death_cert_index():
    es.indices.create(
        index='death_cert',
        body={
            "mappings": {
                'death_cert': {
                    "properties": {
                        'suborder_number': {
                            'type': "keyword"
                        }
                    }
                }
            }
        }
    )


def create_death_cert_docs():
    if not es:
        return
    death_cert = DeathCertificate.query.all()

    operations = []

    for q in death_cert:
        operations.append({
            '_op_type': 'create',
            '_id': q.suborder_number,
            'certificate_number': q.certificate_number,
            'first_name': q.first_name,
            'last_name': q.last_name,
            'middle_name': q.middle_name,
            'num_copies': q.num_copies,
            'cemetery': q.cemetery,
            'month': q.month,
            'day': q.day,
            'years': q.years,
            'death_place': q.death_place,
            'borough': q.borough,
            'letter': q.letter,
            'comment': q.comment,
            'suborder_number': q.suborder_number
        })

    num_success, _ = bulk(
        es,
        operations,
        index='death_cert',
        doc_type='death_cert',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s death certificates docs." % num_success)
