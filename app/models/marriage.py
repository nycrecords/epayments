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
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborder.id'), nullable=False)

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
                suborder_no
    ):
        self.groom_last_name = groom_last_name
        self.groom_first_name = groom_first_name or None
        self.bride_last_name = bride_last_name
        self.bride_first_name = bride_first_name or None
        self.relationship = relationship or None
        self.purpose = purpose
        self.copy_req = copy_req
        self.month = month or None
        self.day = day or None
        self.years = years
        self.marriage_place = marriage_place or None
        self.borough = borough
        self.letter = letter or None
        self.comment = comment or None
        self.suborder_no = suborder_no


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
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborder.id'), nullable=False)

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
            suborder_no
    ):
        self.certificate_no = certificate_no
        self.groom_last_name = groom_last_name
        self.groom_first_name = groom_first_name or None
        self.bride_last_name = bride_last_name
        self.bride_first_name = bride_first_name or None
        self.relationship = relationship or None
        self.purpose = purpose
        self.copy_req = copy_req
        self.month = month or None
        self.day = day or None
        self.years = years or None
        self.marriage_place = marriage_place or None
        self.borough = borough
        self.letter = letter or None
        self.comment = comment or None
        self.suborder_no = suborder_no
