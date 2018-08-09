from app.models import BirthSearch
from app import es
from app.constants.search import RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_birth_search_index():
    es.indices.create(
        index='birth_search',
        body={
            "mappings": {
                'birth_search': {
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


def create_birth_search_docs():
    if not es:
        return
    birth_search = BirthSearch.query.all()

    operations = []

    for q in birth_search:
        operations.append({
            '_op_type': 'create',
            '_id': q.id,
            'id': q.id,
            'first_name': q.first_name,
            'last_name': q.last_name,
            'middle_name': q.middle_name,
            'gender': q.gender,
            'father_name': q.father_name,
            'mother_name': q.mother_name,
            'num_copies': q.num_copies,
            'month': q.month,
            'day': q.day,
            'years': str(q.years),
            'birth_place': q.birth_place,
            'borough': q.borough,
            'letter': q.letter,
            'comment': q.comment,
            'suborder_number': q.suborder_number
        })

    num_success, _ = bulk(
        es,
        operations,
        index='birth_search',
        doc_type='birth_search',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s birth_search docs." % num_success)