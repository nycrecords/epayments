from app import db
from app .constants import purpose, gender
from sqlalchemy.dialects.postgresql import ARRAY


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
    __tablename__ = 'birth_search'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=True)
    last_name = db.Column(db.String(25), nullable=False)
    mid_name = db.Column(db.String(40), nullable=True)
    gender_type = db.Column(
        db.Enum(
            gender.NOT_KNOWN,
            gender.MALE,
            gender.FEMALE,
            name='gender_type'),
        default=gender.NOT_KNOWN)
    father_name = db.Column(db.String(40), nullable=True)
    mother_name = db.Column(db.String(40), nullable=True)
    relationship = db.Column(db.String(30), nullable=True)
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
        default=purpose.OTHER, nullable=False)
    additional_copy = db.Column(db.String(4), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    years = db.Column(ARRAY(db.String(4), dimensions=1))
    birth_place = db.Column(db.String(40), nullable=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False)
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'),
                             nullable=False)

    def __init__(
                self,
                last_name,
                gender_type,
                purpose,
                additional_copy,
                years,
                borough,
                sub_order_no,
                first_name=None,
                mid_name=None,
                father_name=None,
                mother_name=None,
                relationship=None,
                month=None,
                day=None,
                birth_place=None,
                letter=None,
                comment=None

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

    __tablename__ = 'birth_cert'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=True)
    last_name = db.Column(db.String(25), nullable=False)
    mid_name = db.Column(db.String(40), nullable=True)
    gender_type = db.Column(
        db.Enum(
            gender.NOT_KNOWN,
            gender.MALE,
            gender.FEMALE,
            name='gender_type'), default=gender.NOT_KNOWN, nullable=True)
    father_name = db.Column(db.String(40), nullable=True)
    mother_name = db.Column(db.String(40), nullable=True)
    relationship = db.Column(db.String(30), nullable=True)
    purpose = db.Column(
        db.Enum(
            purpose.GENEALOGICAL_HISTORICAL,
            purpose.PERSONAL_USE,
            purpose.LEGAL,
            purpose.IMMIGRATION,
            purpose.MEDICAID_SOCIAL_SECURITY,
            purpose.HEALTH,
            purpose.OTHER,
            name='purpose'), default=purpose.OTHER, nullable=False)
    additional_copy = db.Column(db.String(4), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    years = db.Column(ARRAY(db.String(4), dimensions=1))
    birth_place = db.Column(db.String(40), nullable=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False)
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'),
                             nullable=False)

    def __init__(
            self,
            certificate_no,
            last_name,
            purpose,
            additional_copy,
            years,
            borough,
            sub_order_no,
            first_name=None,
            mid_name=None,
            gender_type=None,
            father_name=None,
            mother_name=None,
            relationship=None,
            month=None,
            day=None,
            birth_place=None,
            letter=None,
            comment=None

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

