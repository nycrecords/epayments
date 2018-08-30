from app.models import PhotoGallery
from app import es
from app.constants.search import RESULTS_CHUNK_SIZE
from elasticsearch.helpers import bulk


def create_photo_gallery_index():
    es.indices.create(
        index='photo_gallery',
        body={
            "mappings": {
                'photo_gallery': {
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


def create_photo_gallery_docs():
    if not es:
        return
    photo_gallery = PhotoGallery.query.all()

    operations = []

    for q in photo_gallery:
        operations.append({
            '_op_type': 'create',
            '_id': q.id,
            'id': q.id,
            "image_id": q.image_id,
            "description": q.description,
            "additional_description": q.additional_description,
            "size": q.size,
            "num_copies": q.num_copies,
            "mail": q.mail,
            "contact_number": q.contact_number,
            "personal_use_agreement": q.personal_use_agreement,
            "comment": q.comment,
            "suborder_number": q.suborder_number,
        })

    num_success, _ = bulk(
        es,
        operations,
        index='photo_gallery',
        doc_type='photo_gallery',
        chunk_size=RESULTS_CHUNK_SIZE,
        raise_on_error=True
    )
    print("Successfully created %s photo gallery docs." % num_success)
