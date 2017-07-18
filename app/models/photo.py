from app import db
from app .constants import borough, collection, size


class PhotoTax(db.Model):
    """

    Define the class with these following relationships

    collection -- Column: enum[]
    borough -- Column: enum[] of the boroughs
    roll -- Column: String(9)
    block -- Column: String(9)
    lot -- Column: String(9)
    street_no -- Column: String(10)
    street -- Column: String(40)
    description -- Column: String(35)
    type -- Column: enum -- size of the photo
    size -- Column: newform -- enum
    copies -- Column: String(2)
    mail_pickup -- Column: Bool
    contact_no -- Column: String(10)
    comment -- Column: String()
    sub_order_no -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'photo_tax'
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
            borough.SATAN_ISLAND,
            borough.BROOKLYN,
            borough.QUEENS,
            name='borough'), default=borough.MANHATTAN, nullable=False)
    roll = db.Column(db.String(9), nullable=True)
    block = db.Column(db.String(9), nullable=True)
    lot = db.Column(db.String(9), nullable=True)
    street_no = db.Column(db.String(10), nullable=False)
    street = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(35), nullable=True)
    type = db.Column(
        db.Enum(
            size.EIGHT_BY_TEN,
            size.ELEVEN_BY_FOURTEEN,
            name='type'), default=size.EIGHT_BY_TEN, nullable=False)
    size = db.Column(
        db.Enum(
            size.EIGHT_BY_TEN,
            size.ELEVEN_BY_FOURTEEN,
            size.SIXTEEN_BY_TWENTY,
            name='size'), default=size.EIGHT_BY_TEN, nullable=True)
    copies = db.Column(db.String(2), nullable=False)
    mail_pickup = db.Column(db.Boolean, nullable=True)
    contact_no = db.Column(db.String(10), nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'),
                             nullable=False)

    def __init__(
                self,
                borough,
                collection,
                street_no,
                street,
                type,
                size,
                copies,
                mail_pickup,
                sub_order_no,
                roll='N/A',
                block='N/A',
                lot='N/A',
                description='N/A',
                contact_no='N/A',
                comment='N/A'

    ):
        self.borough = borough
        self.collection = collection
        self.roll = roll
        self.block = block
        self.lot = lot
        self.street_no = street_no
        self.street = street
        self.description = description
        self.type = type
        self.size = size
        self.copies = copies
        self.mail_pickup = mail_pickup
        self.contact_no = contact_no
        self.comment = comment
        self.sub_order_no = sub_order_no


class PhotoGallery(db.Model):
    """

    Define the class with these following relationships

    image_id -- Column: String(20)
    description -- Column: String(50)
    additional_description -- Column: String(50)
    size -- Column: enum[]
    copy -- Column: String(2)
    mail_pickup -- Column: Bool
    contact_no -- Column: String(10)
    personal_use_agreement -- Column: Bool
    comment -- Column: String(255)
    sub_order_no -- Column: BigInteger, foreignKey

    """

    __tablename = 'photo_gallery'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    additional_description = db.Column(db.String(50), nullable=True)
    size = db.Column(
        db.Enum(
            size.EIGHT_BY_TEN,
            size.ELEVEN_BY_FOURTEEN,
            size.SIXTEEN_BY_TWENTY,
            name='size'), default=size.EIGHT_BY_TEN, nullable=False)
    copy = db.Column(db.String(2), nullable=False)
    mail_pickup = db.Column(db.Boolean, nullable=False)
    contact_no = db.Column(db.String(10), nullable=True)
    personal_use_agreement = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'),
                             nullable=False)

    def __init__(
                self,
                image_id,
                size,
                copy,
                mail_pickup,
                personal_use_agreement,
                sub_order_no,
                description='N/A',
                additional_description='N/A',
                contact_no='N/A',
                comment='N/A'

    ):
        self.image_id = image_id
        self.description = description
        self.additional_description = additional_description
        self.size = size
        self.copy = copy
        self.mail_pickup = mail_pickup
        self.contact_no = contact_no
        self.personal_use_agreement = personal_use_agreement
        self.comment = comment
        self.sub_order_no = sub_order_no
