from app.models import DeathSearch
from app import es
from app.constants.search import RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_death_search_index():
    es.indices.create(
        index='death_search',
        body={
            "mappings": {
                'death_search': {
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


def create_death_search_docs():
    if not es:
        return
    death_search = DeathSearch.query.all()

    operations = []

    for q in death_search:
        operations.append({
            '_op_type': 'create',
            '_id': q.id,
            'id': q.id,
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
        index='death_search',
        doc_type='death_search',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s death search docs." % num_success)
