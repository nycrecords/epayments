from app import db
from app .constants import purpose
from sqlalchemy.dialects.postgresql import ARRAY


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
    suborder_no -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'death_search'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(40), nullable=True)
    mid_name = db.Column(db.String(40), nullable=True)
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
    copy_req = db.Column(db.String(40), nullable=True)
    cemetery = db.Column(db.String(40), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=True)
    death_place = db.Column(db.String(40), nullable=True)
    age_of_death = db.Column(db.String(3), nullable=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False)
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborder.id'), nullable=False)

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
                suborder_no
    ):
        self.last_name = last_name
        self.first_name = first_name or None
        self.mid_name = mid_name or None
        self.relationship = relationship or None
        self.purpose = purpose
        self.copy_req = copy_req or None
        self.cemetery = cemetery or None
        self.month = month or None
        self.day = day or None
        self.years = years or None
        self.death_place = death_place or None
        self.age_of_death = age_of_death or None
        self.borough = borough
        self.letter = letter or None
        self.comment = comment or None
        self.suborder_no = suborder_no


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
    suborder_no -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'death_cert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_no = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(40), nullable=True)
    mid_name = db.Column(db.String(40), nullable=True)
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
    copy_req = db.Column(db.String(40), nullable=True)
    cemetery = db.Column(db.String(40), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=True)
    death_place = db.Column(db.String(40), nullable=True)
    age_of_death = db.Column(db.String(3), nullable=True)
    borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False)
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_no = db.Column(db.BigInteger, db.ForeignKey('suborder.id'), nullable=False)

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
            suborder_no
    ):
        self.certificate_no = certificate_no
        self.last_name = last_name
        self.first_name = first_name or None
        self.mid_name = mid_name or None
        self.relationship = relationship or None
        self.purpose = purpose
        self.copy_req = copy_req or None
        self.cemetery = cemetery or None
        self.month = month or None
        self.day = day or None
        self.years = years
        self.death_place = death_place or None
        self.age_of_death = age_of_death or None
        self.borough = borough
        self.letter = letter or None
        self.comment = comment or None
        self.suborder_no = suborder_no
