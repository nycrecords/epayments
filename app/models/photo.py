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
    suborder_no -- Column: BigInteger, foreignKey

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
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborder.id'), nullable=False)

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
                suborder_no
    ):
        self.borough = borough
        self.collection = collection
        self.roll = roll or 'N/A'
        self.block = block or 'N/A'
        self.lot = lot or 'N/A'
        self.street_no = street_no
        self.street = street
        self.description = description or 'N/A'
        self.type = type
        self.size = size
        self.copies = copies
        self.mail_pickup = mail_pickup
        self.contact_no = contact_no or 'N/A'
        self.comment = comment or 'N/A'
        self.suborder_no = suborder_no


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
    suborder_no -- Column: BigInteger, foreignKey

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
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborder.id'), nullable=False)

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
                suborder_no
    ):
        self.image_id = image_id
        self.description = description or 'N/A'
        self.additional_description = additional_description or 'N/A'
        self.size = size
        self.copy = copy
        self.mail_pickup = mail_pickup
        self.contact_no = contact_no or 'N/A'
        self.personal_use_agreement = personal_use_agreement
        self.comment = comment or 'N/A'
        self.suborder_no = suborder_no
