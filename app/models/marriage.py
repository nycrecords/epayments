from app import db
from app .constants import purpose
from sqlalchemy.dialects.postgresql import ARRAY


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
    copy_req -- Column: string // put as 40 because new one is 40
    month -- Column: string
    day -- Column: string
    year -- Column: enum[5 years]
    marriage_place -- Column: String(40)
    borough -- Column: String/Array?
    letter -- Column: bool
    comment -- Column: String(255)
    sub_order_num -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'marriage_search'
    id = db.Column(db.Integer, primary_key=True)
    groom_last_name = db.Column(db.String(25), nullable=False)
    groom_first_name = db.Column(db.String(40), nullable=True)
    bride_last_name = db.Column(db.String(25), nullable=False)
    bride_first_name = db.Column(db.String(40), nullable=True)
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
    copy_req = db.Column(db.String(40), nullable=False)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=False)
    marriage_place = db.Column(db.String(40), nullable=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False)
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'),
                             nullable=False)

    def __init__(
                self,
                groom_last_name,
                bride_last_name,
                purpose,
                copy_req,
                years,
                borough,
                sub_order_no,
                groom_first_name=None,
                bride_first_name=None,
                relationship=None,
                month=None,
                day=None,
                marriage_place=None,
                letter=None,
                comment=None

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

    __tablename__ = 'marriage_cert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_no = db.Column(db.String(40))
    groom_last_name = db.Column(db.String(25), nullable=False)
    groom_first_name = db.Column(db.String(40), nullable=True)
    bride_last_name = db.Column(db.String(25), nullable=False)
    bride_first_name = db.Column(db.String(40), nullable=True)
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
    copy_req = db.Column(db.String(40), nullable=False)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=True)
    marriage_place = db.Column(db.String(40), nullable=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False)
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    sub_order_no = db.Column(db.BigInteger, db.ForeignKey('orders.sub_order_no'),
                             nullable=False)

    def __init__(
            self,
            certificate_no,
            groom_last_name,
            bride_last_name,
            purpose,
            copy_req,
            borough,
            sub_order_no,
            groom_first_name=None,
            bride_first_name=None,
            relationship=None,
            month=None,
            day=None,
            years=None,
            marriage_place=None,
            letter=None,
            comment=None

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