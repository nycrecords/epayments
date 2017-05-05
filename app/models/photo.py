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

    __tablename__ = 'photoTax'
    id = db.Column(db.Integer, primary_key=True)
    collection = db.Column(
        db.Enum(
            collection.YEAR_1940,
            collection.YEAR_1980,
            collection.BOTH,
            name='collection'))
    borough = db.Column(
        db.Enum(
            borough.BRONX,
            borough.MANHATTAN,
            borough.SATAN_ISLAND,
            borough.BROOKLYN,
            borough.QUEENS,
            name='borough'))
    roll = db.Column(db.String(9))
    block = db.Column(db.String(9))
    lot = db.Column(db.String(9))
    street_no = db.Column(db.String(10))
    street = db.Column(db.String(40))
    description = db.Column(db.String(35))
    type = db.Column(
        db.Enum(
            size.EIGHT_BY_TEN,
            size.ELEVEN_BY_FOURTEEN,
            name='type'))
    size = db.Column(
        db.Enum(
            size.EIGHT_BY_TEN,
            size.ELEVEN_BY_FOURTEEN,
            size.SIXTEEN_BY_TWENTY,
            name='size'))
    copies = db.Column(db.String(2))
    mail_pickup = db.Column(db.Boolean)
    contact_no = db.Column(db.String(10))
    comment = db.Column(db.String(255))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
                self,
                borough,
                collection,
                roll,
                block,
                lot,
                street_no,
                street,
                description,
                type,
                size,
                copies,
                mail_pickup,
                contact_no,
                comment,
                sub_order_no
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

    __tablename = 'photoGallery'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(20))
    description = db.Column(db.String(50))
    additional_description = db.Column(db.String(50))
    size = db.Column(
        db.Enum(
            size.EIGHT_BY_TEN,
            size.ELEVEN_BY_FOURTEEN,
            size.SIXTEEN_BY_TWENTY,
            name='size'))
    copy = db.Column(db.String(2))
    mail_pickup = db.Column(db.Boolean)
    contact_no = db.Column(db.String(10))
    personal_use_agreement = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
                self,
                image_id,
                description,
                additional_description,
                size,
                copy,
                mail_pickup,
                contact_no,
                personal_use_agreement,
                comment,
                sub_order_no
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
