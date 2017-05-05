from sqlalchemy.dialects.postgresql import ARRAY

from app import db
from app._constants_ import borough, collection, gender, purpose, size, status


class Orders(db.Model):
    """
    Define the new Order class with the following Columns & relationships

    order_number -- Column: String(64)
    sub_order_no -- Column: BigInteger, PrimaryKey
    date_submitted -- Column: DateTime -- date order was submitted
    date_received -- Column: DateTime -- day we receive order
    billing_name -- Column: String(64)
    customer_email -- Column: String(64)
    confirmation_message -- Column: Text
    client_data -- Column: Text

    """

    __tablename__ = 'orders'
    order_no = db.Column(db.String(64))
    sub_order_no = db.Column(db.BigInteger, primary_key=True)
    date_submitted = db.Column(db.DateTime)
    date_received = db.Column(db.DateTime)
    billing_name = db.Column(db.String(64))
    customer_email = db.Column(db.String(64))
    confirmation_message = db.Column(db.Text)
    client_data = db.Column(db.Text)

    def __init__(
            self,
            order_no,
            sub_order_no,
            date_submitted,
            date_receivied,
            billing_name,
            customer_email,
            confirmation_message,
            client_data

    ):
        self.order_no = order_no
        self.sub_order_no = sub_order_no
        self.date_submitted = date_submitted
        self.date_submitted = date_receivied
        self.billing_name = billing_name
        self.customer_email = customer_email
        self.confirmation_message = confirmation_message
        self.client_data = client_data


class StatusTracker(db.Model):

    """
    Need to make a model that will change the status of the
    process of the document

    id - db.Integer , primary key = true
    sub_order_no - Column: BigInteger, Foreign Key - connects the sub_order# to the top of this database
    status - Column: Enum - Tracks the status of the order can only be these set things

    1. Received || Set to this by default
    2. Processing
        a)found
        b)printed
    3. Mailed/Pickup
    4. Not_Found
        a)Letter_generated
        b)Undeliverable - Cant move down the line
    5. Done - End of status changes

    """

    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))
    current_status = db.Column(
        db.Enum(
            status.RECEIVED,
            status.PROCESSING,
            status.FOUND,
            status.MAILED_PICKUP,
            status.NOT_FOUND,
            status.LETTER_GENERATED,
            status.UNDELIVERABLE,
            status.DONE,
            name='current_status'),
        default=status.RECEIVED)

    # Class Constructor to initialize the data
    def __init__(
                self,
                sub_order_no
    ):
        self.sub_order_no = sub_order_no


class Shipping(db.Model):

    """
    Define the Shipping class with the following columns and relationships:

    name -- Column: String(64)
    address_Line_1 -- Column: String(64)
    address_Line_1 -- Column: String(64)
    city -- Column: String(64)
    state -- Column: String(64)
    zip -- Column: String(64)
    country -- Column: String(64)
    phone -- Column: String(64)
    instructions -- Column: String(64)
    order_no -- Column: String(64), foreignKey

    """
    __tablename__ = 'shipping'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    address_line_1 = db.Column(db.String(64))
    address_line_2 = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip_code = db.Column(db.String(64))
    country = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    instructions = db.Column(db.String(64))

    def __init__(
                self,
                name,
                address_line_1,
                address_line_2,
                city,
                state,
                zip_code,
                country,
                phone,
                instructions

    ):
        self.name = name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone = phone
        self.instructions = instructions


class BirthSearch(db.Model):
    """

    Define the class with these following relationships

    first_name -- Column: String(40)
    last_name -- Column: String(25)
    mid_name -- Column: String(40)
    gender -- Column: enum[M,F]
    father_name -- Column: string(40)
    mother_name -- Column: string(40)
    relationship -- Column: string(string)
    purpose -- Column: enum[]
    additional_copy -- Column: string // put as 40 new one is 40
    month -- Column: string
    day -- Column: string
    years -- Column: array[5 max years can be put here]
    birth_place -- Column: String(40)
    borough -- Column: array[5] 1-D
    letter -- Column: Bool
    comment -- Column: string(255)
    sub_order_no -- Column: BigInteger, foreignKey
    """
    __tablename__ = 'birthSearch'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(25))
    mid_name = db.Column(db.String(40))
    gender_type = db.Column(
        db.Enum(
            gender.NOT_KNOWN,
            gender.MALE,
            gender.FEMALE,
            name='gender_type'),
        default=gender.NOT_KNOWN)
    father_name = db.Column(db.String(40))
    mother_name = db.Column(db.String(40))
    relationship = db.Column(db.String(30))
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'),
        default=purpose.OTHER)
    additional_copy = db.Column(db.String(4))
    month = db.Column(db.String(20))
    day = db.Column(db.String(3))
    years = db.Column(ARRAY(db.String(4), dimensions=1))
    birth_place = db.Column(db.String(40))
    borough = db.Column(ARRAY(db.String(20), dimensions=1))
    letter = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
                self,
                first_name,
                last_name,
                mid_name,
                gender_type,
                father_name,
                mother_name,
                relationship,
                purpose,
                additional_copy,
                month,
                day,
                years,
                birth_place,
                borough,
                letter,
                comment,
                sub_order_no
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.mid_name = mid_name
        self.gender_type = gender_type
        self.father_name = father_name
        self.mother_name = mother_name
        self.relationship = relationship
        self.purpose = purpose
        self.additional_copy = additional_copy
        self.month = month
        self.day = day
        self.years = years
        self.birth_place = birth_place
        self.borough = borough
        self.letter = letter
        self.comment = comment
        self.sub_order_no = sub_order_no


class MarriageSearch(db.Model):
    """

    Define the class with these following relationships

    groom_last_name -- Column: String(25)
    groom_first_name -- Column: String(40)
    bride_last_name -- Column: String(25)
    bride_first_name -- Column: String(40)
    relationship -- Column: String(30)
    purpose -- Column: enum[Genealogical/Historical, Personal Use, Legal, Immigration, Medicaid/Social Security
                            Health, Other] 7 Total different selection fields
    copy_req -- Column: string // put as 40 cause new one is 40
    month -- Column: string
    day -- Column: string
    year -- Column: enum[5 years]
    marriage_place -- Column: String(40)
    borough -- Column: String/Array?
    letter -- Column: bool
    comment -- Column: String(255)
    sub_order_num -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'marriageSearch'
    id = db.Column(db.Integer, primary_key=True)
    groom_last_name = db.Column(db.String(25))
    groom_first_name = db.Column(db.String(40))
    bride_last_name = db.Column(db.String(25))
    bride_first_name = db.Column(db.String(40))
    relationship = db.Column(db.String(30))
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'),
        default=purpose.OTHER)
    copy_req = db.Column(db.String(40))
    month = db.Column(db.String(20))
    day = db.Column(db.String(2))
    years = db.Column(ARRAY(db.String(4), dimensions=1))
    marriage_place = db.Column(db.String(40))
    borough = db.Column(ARRAY(db.String(20), dimensions=1))
    letter = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
                self,
                groom_last_name,
                groom_first_name,
                bride_last_name,
                bride_first_name,
                relationship,
                purpose,
                copy_req,
                month,
                day,
                years,
                marriage_place,
                borough,
                letter,
                comment,
                sub_order_no
    ):
        self.groom_last_name = groom_last_name
        self.groom_first_name = groom_first_name
        self.bride_last_name = bride_last_name
        self.bride_first_name = bride_first_name
        self.relationship = relationship
        self.purpose = purpose
        self.copy_req = copy_req
        self.month = month
        self.day = day
        self.years = years
        self.marriage_place = marriage_place
        self.borough = borough
        self.letter = letter
        self.comment = comment
        self.sub_order_no = sub_order_no


class DeathSearch(db.Model):
    """

    Define the class with these following relationships

    last_name -- Column: String(25)
    first_name -- Column: String(40)
    mid_name -- Column: String(40)
    relationship -- Column: String(30)
    purpose -- Column: enum[]
    copy_req -- Column: String(2) // put as 40 because new one is 40
    cemetery -- Column: String(40)
    month -- Column: string
    day -- Column: string
    year -- Column: array[]
    death_place -- Column: String(40)
    age_of_death -- Column: String(3)
    borough -- Column: String/Array
    letter -- Column: bool
    comment -- Column: String(255)
    sub_order_no -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'deathSearch'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(25))
    first_name = db.Column(db.String(40))
    mid_name = db.Column(db.String(40))
    relationship = db.Column(db.String(30))
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'),
        default=purpose.OTHER)
    copy_req = db.Column(db.String(40))
    cemetery = db.Column(db.String(40))
    month = db.Column(db.String(20))
    day = db.Column(db.String(2))
    years = db.Column(ARRAY(db.String(4), dimensions=1))
    death_place = db.Column(db.String(40))
    age_of_death = db.Column(db.String(3))
    borough = db.Column(ARRAY(db.String(20), dimensions=1))
    letter = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
                self,
                last_name,
                first_name,
                mid_name,
                relationship,
                purpose,
                copy_req,
                cemetery,
                month,
                day,
                years,
                death_place,
                age_of_death,
                borough,
                letter,
                comment,
                sub_order_no
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.mid_name = mid_name
        self.relationship = relationship
        self.purpose = purpose
        self.copy_req = copy_req
        self.cemetery = cemetery
        self.month = month
        self.day = day
        self.years = years
        self.death_place = death_place
        self.age_of_death = age_of_death
        self.borough = borough
        self.letter = letter
        self.comment = comment
        self.sub_order_no = sub_order_no


class BirthCertificate(db.Model):
    """

    Define the class with these following relationships

    certificate_num -- Column: String(40)
    first_name -- Column: String(40)
    last_name -- Column: String(25)
    mid_name -- Column: String(40)
    gender -- Column: enum[M,F]
    father_name -- Column: string(40)
    mother_name -- Column: string(40)
    relationship -- Column: string(string)
    purpose -- Column: enum[]
    additional_copy -- Column: String(40)
    month -- Column: string
    day -- Column: string
    years -- Column: array[5 max years can be put here]
    birth_place -- Column: String(40)
    borough -- Column: array[]
    letter -- Column: Bool
    comment -- Column: string(255)
    sub_order_no -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'birthCert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_no = db.Column(db.String(40))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(25))
    mid_name = db.Column(db.String(40))
    gender_type = db.Column(
        db.Enum(
            gender.NOT_KNOWN,
            gender.MALE,
            gender.FEMALE,
            name='gender_type'),
        default=gender.NOT_KNOWN)
    father_name = db.Column(db.String(40))
    mother_name = db.Column(db.String(40))
    relationship = db.Column(db.String(30))
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'),
        default=purpose.OTHER)
    additional_copy = db.Column(db.String(40))
    month = db.Column(db.String(20))
    day = db.Column(db.String(2))
    years = db.Column(ARRAY(db.String(4), dimensions=1))
    birth_place = db.Column(db.String(40))
    borough = db.Column(ARRAY(db.String(20), dimensions=1))
    letter = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
            self,
            certificate_no,
            first_name,
            last_name,
            mid_name,
            gender_type,
            father_name,
            mother_name,
            relationship,
            purpose,
            additional_copy,
            month,
            day,
            years,
            birth_place,
            borough,
            letter,
            comment,
            sub_order_no
    ):
        self.certificate_no = certificate_no
        self.first_name = first_name
        self.last_name = last_name
        self.mid_name = mid_name
        self.gender_type = gender_type
        self.father_name = father_name
        self.mother_name = mother_name
        self.relationship = relationship
        self.purpose = purpose
        self.additional_copy = additional_copy
        self.month = month
        self.day = day
        self.years = years
        self.birth_place = birth_place
        self.borough = borough
        self.letter = letter
        self.comment = comment
        self.sub_order_no = sub_order_no


class MarriageCertificate(db.Model):
    """

    Define the class with these following relationships

    certificate_num -- Column: String(40)
    groom_last_name -- Column: String(25)
    groom_first_name -- Column: String(40)
    bride_last_name -- Column: String(25)
    bride_first_name -- Column: String(40)
    relationship -- Column: String(30)
    purpose -- Column: enum[]
    copy_req -- Column: String(40)
    month -- Column: string
    day -- Column: string
    year -- Column: enum[5 years]
    marriage_place -- Column: String(40)
    borough -- Column: String/Array?
    letter -- Column: Bool
    comment -- Column: String(255)
    sub_order_num -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'marriageCert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_no = db.Column(db.String(40))
    groom_last_name = db.Column(db.String(25))
    groom_first_name = db.Column(db.String(40))
    bride_last_name = db.Column(db.String(25))
    bride_first_name = db.Column(db.String(40))
    relationship = db.Column(db.String(30))
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'),
        default=purpose.OTHER)
    copy_req = db.Column(db.String(40))
    month = db.Column(db.String(20))
    day = db.Column(db.String(2))
    years = db.Column(ARRAY(db.String(4), dimensions=1))
    marriage_place = db.Column(db.String(40))
    borough = db.Column(ARRAY(db.String(20), dimensions=1))
    letter = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
            self,
            certificate_no,
            groom_last_name,
            groom_first_name,
            bride_last_name,
            bride_first_name,
            relationship,
            purpose,
            copy_req,
            month,
            day,
            years,
            marriage_place,
            borough,
            letter,
            comment,
            sub_order_no
    ):
        self.certificate_no = certificate_no
        self.groom_last_name = groom_last_name
        self.groom_first_name = groom_first_name
        self.bride_last_name = bride_last_name
        self.bride_first_name = bride_first_name
        self.relationship = relationship
        self.purpose = purpose
        self.copy_req = copy_req
        self.month = month
        self.day = day
        self.years = years
        self.marriage_place = marriage_place
        self.borough = borough
        self.letter = letter
        self.comment = comment
        self.sub_order_no = sub_order_no


class DeathCertificate(db.Model):
    """

    Define the class with these following relationships

    certificate_num -- Column: String(40)
    last_name -- Column: String(25)
    first_name -- Column: String(40)
    mid_name -- Column: String(40)
    relationship -- Column: String(30)
    purpose -- Column: enum[]
    copy_req -- Column: String(40)
    cemetery -- Column: String(40)
    month -- Column: string
    day -- Column: string
    year -- Column: array[]
    death_place -- Column: String(40)
    age_of_death -- Column: String(3)
    borough -- Column: String/Array
    letter -- Column: bool
    comment -- Column: String(255)
    sub_order_no -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'deathCert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_no = db.Column(db.String(40))
    last_name = db.Column(db.String(25))
    first_name = db.Column(db.String(40))
    mid_name = db.Column(db.String(40))
    relationship = db.Column(db.String(30))
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'),
        default=purpose.OTHER)
    copy_req = db.Column(db.String(40))
    cemetery = db.Column(db.String(40))
    month = db.Column(db.String(20))
    day = db.Column(db.String(2))
    years = db.Column(ARRAY(db.String(4), dimensions=1))
    death_place = db.Column(db.String(40))
    age_of_death = db.Column(db.String(3))
    borough = db.Column(ARRAY(db.String(20), dimensions=1))
    letter = db.Column(db.Boolean)
    comment = db.Column(db.String(255))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
            self,
            certificate_no,
            last_name,
            first_name,
            mid_name,
            relationship,
            purpose,
            copy_req,
            cemetery,
            month,
            day,
            years,
            death_place,
            age_of_death,
            borough,
            letter,
            comment,
            sub_order_no
    ):
        self.certificate_no = certificate_no
        self.last_name = last_name
        self.first_name = first_name
        self.mid_name = mid_name
        self.relationship = relationship
        self.purpose = purpose
        self.copy_req = copy_req
        self.cemetery = cemetery
        self.month = month
        self.day = day
        self.years = years
        self.death_place = death_place
        self.age_of_death = age_of_death
        self.borough = borough
        self.letter = letter
        self.comment = comment
        self.sub_order_no = sub_order_no


class PropertyCard(db.Model):
    """

    Define the class with these following relationships

    borough -- Column: String/Array   //// IS THIS AN ARRAY or ENUM
    block -- Column: String(9)
    lot -- Column: String(9)
    building_no -- Column: String(10)
    street -- Column: String(40)
    description -- Column: String(35)
    certified -- Column: Bool
    mail_pickup -- Column: Bool
    comment -- Column: String(35)
    sub_order_no -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'propCard'
    id = db.Column(db.Integer, primary_key=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1))
    block = db.Column(db.String(9))
    lot = db.Column(db.String(9))
    building_no = db.Column(db.String(10))
    street = db.Column(db.String(40))
    description = db.Column(db.String(40))
    certified = db.Column(db.Boolean)
    mail_pickup = db.Column(db.Boolean)
    comment = db.Column(db.String(35))
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'))

    def __init__(
                self,
                borough,
                block,
                lot,
                building_no,
                street,
                description,
                certified,
                mail_pickup,
                comment,
                sub_order_no
    ):
        self.borough = borough
        self.block = block
        self.lot = lot
        self.building_no = building_no
        self.street = street
        self.description = description
        self.certified = certified
        self.mail_pickup = mail_pickup
        self.comment = comment
        self.sub_order_no = sub_order_no


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
