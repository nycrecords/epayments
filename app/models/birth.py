from app import db
from app.constants import purpose, gender
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
    num_copies -- Column: string // put as 40 new one is 40
    month -- Column: string
    day -- Column: string
    years -- Column: array[5 max years can be put here]
    birth_place -- Column: String(40)
    borough -- Column: array[5] 1-D
    letter -- Column: Bool
    comment -- Column: string(255)
    suborder_number -- Column: BigInteger, foreignKey
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
    num_copies = db.Column(db.String(4), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), name='years')
    birth_place = db.Column(db.String(40), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborder.id'), nullable=False)

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
            num_copies,
            month,
            day,
            years,
            birth_place,
            borough,
            letter,
            comment,
            suborder_number
    ):
        self.first_name = first_name or None
        self.last_name = last_name
        self.mid_name = mid_name or None
        self.gender_type = gender_type
        self.father_name = father_name or None
        self.mother_name = mother_name or None
        self.relationship = relationship or None
        self.purpose = purpose
        self.num_copies = num_copies
        self.month = month or None
        self.day = day or None
        self._years = years
        self.birth_place = birth_place or None
        self._borough = borough
        self.letter = letter or None
        self.comment = comment or None
        self.suborder_number = suborder_number

    @property
    def years(self):
        if isinstance(self._years, list):
            if len(self._years) > 1:
                return ",".join(self._years)
            else:
                return self._years[0]
        else:
            return None

    @years.setter
    def years(self, value):
        self._years = value

    @property
    def borough(self):
        if len(self._borough) > 1:
            _ = ''
            for year in self._borough:
                _ = "{}, {}".format(year, _)
        else:
            return self._borough[0]

    @borough.setter
    def borough(self, value):
        self._borough = value

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'mid_name': self.mid_name,
            'gender_type': self.gender_type,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'relationship': self.relationship,
            'purpose': self.purpose,
            'num_copies': self.num_copies,
            'month': self.month,
            'day': self.day,
            'years': str(self.years),
            'birth_place': self.birth_place,
            'borough': self.borough,
            'letter': self.letter,
            'comment': self.comment,
            'suborder_number': self.suborder_number
        }


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
    num_copies -- Column: String(40)
    month -- Column: string
    day -- Column: string
    years -- Column: array[5 max years can be put here]
    birth_place -- Column: String(40)
    borough -- Column: array[]
    letter -- Column: Bool
    comment -- Column: string(255)
    suborder_number -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'birth_cert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_no = db.Column(db.String(40), nullable=False)
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
    num_copies = db.Column(db.String(4), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), name='years')
    birth_place = db.Column(db.String(40), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborder.id'), nullable=False)

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
            num_copies,
            month,
            day,
            years,
            birth_place,
            borough,
            letter,
            comment,
            suborder_number
    ):
        self.certificate_no = certificate_no
        self.first_name = first_name or None
        self.last_name = last_name
        self.mid_name = mid_name or None
        self.gender_type = gender_type or None
        self.father_name = father_name or None
        self.mother_name = mother_name or None
        self.relationship = relationship or None
        self.purpose = purpose
        self.num_copies = num_copies
        self.month = month or None
        self.day = day or None
        self._years = years
        self.birth_place = birth_place or None
        self._borough = [borough]
        self.letter = letter or None
        self.comment = comment or None
        self.suborder_number = suborder_number

    @property
    def years(self):
        if isinstance(self._years, list):
            if len(self._years) > 1:
                return ",".join(self._years)
            else:
                return self._years[0]
        else:
            return None

    @years.setter
    def years(self, value):
        self._years = value

    @property
    def borough(self):
        if len(self._borough) > 1:
            _ = ''
            for year in self._borough:
                _ = "{}, {}".format(year, _)
        else:
            return self._borough[0]

    @borough.setter
    def borough(self, value):
        self._borough = value

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'certificate_no': self.certificate_no,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'mid_name': self.mid_name,
            'gender_type': self.gender_type,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'relationship': self.relationship,
            'purpose': self.purpose,
            'num_copies': self.num_copies,
            'month': self.month,
            'day': self.day,
            'years': str(self.years),
            'birth_place': self.birth_place,
            'borough': self.borough,
            'letter': self.letter,
            'comment': self.comment,
            'suborder_number': self.suborder_number
        }
