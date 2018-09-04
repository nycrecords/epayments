from app import db, es
from app.constants import borough, collection, size


class TaxPhoto(db.Model):
    """
    Define the class with these following relationships

    collection -- Column: enum[]
    borough -- Column: enum[] of the boroughs
    roll -- Column: String(9)
    block -- Column: String(9)
    lot -- Column: String(9)
    building_number -- Column: String(10)
    street -- Column: String(40)
    description -- Column: String(35)
    type -- Column: enum -- size of the photo
    size -- Column: newform -- enum
    num_copies -- Column: String(2)
    mail -- Column: Bool
    contact_number -- Column: String(10)
    suborder_number -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'tax_photo'
    id = db.Column(db.Integer, primary_key=True)
    collection = db.Column(
        db.Enum(
            collection.YEAR_1940,
            collection.YEAR_1980,
            collection.BOTH,
            name='collection'), default=collection.BOTH, nullable=False)
    borough = db.Column(
        db.Enum(
            borough.BRONX,
            borough.MANHATTAN,
            borough.STATEN_ISLAND,
            borough.BROOKLYN,
            borough.QUEENS,
            name='borough'), default=borough.MANHATTAN, nullable=False)
    roll = db.Column(db.String(9), nullable=True)
    block = db.Column(db.String(9), nullable=True)
    lot = db.Column(db.String(9), nullable=True)
    building_number = db.Column(db.String(10), nullable=False)
    street = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(35), nullable=True)
    size = db.Column(
        db.Enum(
            size.EIGHT_BY_TEN,
            size.ELEVEN_BY_FOURTEEN,
            name='size'), nullable=False)
    num_copies = db.Column(db.String(2), nullable=False)
    mail = db.Column(db.Boolean, nullable=False)
    contact_number = db.Column(db.String(10), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            borough,
            collection,
            roll,
            block,
            lot,
            building_number,
            street,
            description,
            size,
            num_copies,
            mail,
            contact_number,
            suborder_number
    ):
        self.borough = borough
        self.collection = collection
        self.roll = roll
        self.block = block
        self.lot = lot
        self.building_number = building_number
        self.street = street
        self.description = description
        self.size = size
        self.num_copies = num_copies
        self.mail = mail
        self.contact_number = contact_number
        self.suborder_number = suborder_number

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'borough': self.borough,
            'collection': self.collection,
            'roll': self.roll,
            'block': self.block,
            'lot': self.lot,
            'building_number': self.building_number,
            'street': self.street,
            'description': self.description,
            'size': self.size,
            'num_copies': self.num_copies,
            'mail': self.mail,
            'contact_number': self.contact_number,
            'suborder_number': self.suborder_number,
        }

    def es_create(self):
        es.create(
            index='tax_photo',
            doc_type='tax_photo',
            id=self.suborder_number,
            body={
                'borough': self.borough,
                'collection': self.collection,
                'roll': self.roll,
                'block': self.block,
                'lot': self.lot,
                'building_number': self.building_number,
                'street': self.street,
                'description': self.description,
                'size': self.size,
                'num_copies': self.num_copies,
                'mail': self.mail,
                'contact_number': self.contact_number,
                'suborder_number': self.suborder_number,
            }
        )


class PhotoGallery(db.Model):
    """
    Define the class with these following relationships

    image_id -- Column: String(20)
    description -- Column: String(50)
    additional_description -- Column: String(50)
    size -- Column: enum[]
    copy -- Column: String(2)
    mail -- Column: Bool
    contact_number -- Column: String(10)
    personal_use_agreement -- Column: Bool
    comment -- Column: String(255)
    suborder_number -- Column: BigInteger, foreignKey

    """

    __tablename = 'photo_gallery'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    additional_description = db.Column(db.String(500), nullable=True)
    size = db.Column(
        db.Enum(
            size.EIGHT_BY_TEN,
            size.ELEVEN_BY_FOURTEEN,
            size.SIXTEEN_BY_TWENTY,
            name='size'), nullable=False)
    num_copies = db.Column(db.String(2), nullable=False)
    mail = db.Column(db.Boolean, nullable=False)
    contact_number = db.Column(db.String(10), nullable=True)
    personal_use_agreement = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            image_id,
            description,
            additional_description,
            size,
            num_copies,
            mail,
            contact_number,
            personal_use_agreement,
            comment,
            suborder_number
    ):
        self.image_id = image_id
        self.description = description
        self.additional_description = additional_description
        self.size = size
        self.num_copies = num_copies
        self.mail = mail
        self.contact_number = contact_number
        self.personal_use_agreement = personal_use_agreement
        self.comment = comment
        self.suborder_number = suborder_number

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "image_id": self.image_id,
            "description": self.description,
            "additional_description": self.additional_description,
            "size": self.size,
            "num_copies": self.num_copies,
            "mail": self.mail,
            "contact_number": self.contact_number,
            "personal_use_agreement": self.personal_use_agreement,
            "comment": self.comment,
            "suborder_number": self.suborder_number,
        }

    def es_create(self):
        es.create(
            index='photo_gallery',
            doc_type='photo_gallery',
            id=self.suborder_number,
            body={
                'image_id': self.image_id,
                'description': self.description,
                'additional_description': self.additional_description,
                'size': self.size,
                'num_copies': self.num_copies,
                'mail': self.mail,
                'contact_number': self.contact_number,
                'personal_use_agreement': self.personal_use_agreement,
                'comment': self.comment,
                'suborder_number': self.suborder_number
            }
        )
