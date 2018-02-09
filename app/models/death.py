from app import db
from sqlalchemy.dialects.postgresql import ARRAY


class DeathSearch(db.Model):
    """

    Define the class with these following relationships

    last_name -- Column: String(25)
    first_name -- Column: String(40)
    mid_name -- Column: String(40)
    num_copies -- Column: String(2) // put as 40 because new one is 40
    cemetery -- Column: String(40)
    month -- Column: string
    day -- Column: string
    year -- Column: array[]
    death_place -- Column: String(40)
    age_of_death -- Column: String(3)
    borough -- Column: String/Array
    letter -- Column: bool
    comment -- Column: String(255)
    suborder_number -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'death_search'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(40), nullable=True)
    mid_name = db.Column(db.String(40), nullable=True)
    num_copies = db.Column(db.String(40), nullable=True)
    cemetery = db.Column(db.String(40), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=True, name='years')
    death_place = db.Column(db.String(40), nullable=True)
    age_of_death = db.Column(db.String(3), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            last_name,
            first_name,
            mid_name,
            num_copies,
            cemetery,
            month,
            day,
            years,
            death_place,
            age_of_death,
            borough,
            letter,
            comment,
            suborder_number
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.mid_name = mid_name
        self.num_copies = num_copies or None
        self.cemetery = cemetery or None
        self.month = month or None
        self.day = day or None
        self._years = years or None
        self.death_place = death_place or None
        self.age_of_death = age_of_death or None
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
            'num_copies': self.num_copies,
            'cemetery': self.cemetery,
            'month': self.month,
            'day': self.day,
            'years': self.years,
            'death_place': self.death_place,
            'age_of_death': self.age_of_death,
            'borough': self.borough,
            'letter': self.letter,
            'comment': self.comment,
            'suborder_number': self.suborder_number
        }


class DeathCertificate(db.Model):
    """

    Define the class with these following relationships

    certificate_num -- Column: String(40)
    last_name -- Column: String(25)
    first_name -- Column: String(40)
    mid_name -- Column: String(40)
    num_copies -- Column: String(40)
    cemetery -- Column: String(40)
    month -- Column: string
    day -- Column: string
    year -- Column: array[]
    death_place -- Column: String(40)
    age_of_death -- Column: String(3)
    borough -- Column: String/Array
    letter -- Column: bool
    comment -- Column: String(255)
    suborder_number -- Column: BigInteger, foreignKey

    """

    __tablename__ = 'death_cert'
    id = db.Column(db.Integer, primary_key=True)
    certificate_no = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(40), nullable=True)
    mid_name = db.Column(db.String(40), nullable=True)
    num_copies = db.Column(db.String(40), nullable=True)
    cemetery = db.Column(db.String(40), nullable=True)
    month = db.Column(db.String(20), nullable=True)
    day = db.Column(db.String(2), nullable=True)
    _years = db.Column(ARRAY(db.String(4), dimensions=1), nullable=True, name='years')
    death_place = db.Column(db.String(40), nullable=True)
    age_of_death = db.Column(db.String(3), nullable=True)
    _borough = db.Column(ARRAY(db.String(20), dimensions=1), nullable=False, name='borough')
    letter = db.Column(db.Boolean, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    suborder_number = db.Column(db.String(32), db.ForeignKey('suborders.id'), nullable=False)

    def __init__(
            self,
            certificate_no,
            last_name,
            first_name,
            mid_name,
            num_copies,
            cemetery,
            month,
            day,
            years,
            death_place,
            age_of_death,
            borough,
            letter,
            comment,
            suborder_number
    ):
        self.certificate_no = certificate_no
        self.last_name = last_name
        self.first_name = first_name
        self.mid_name = mid_name
        self.num_copies = num_copies or None
        self.cemetery = cemetery or None
        self.month = month or None
        self.day = day or None
        self._years = years
        self.death_place = death_place or None
        self.age_of_death = age_of_death or None
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
            'certificate_no': self.certificate_no,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'mid_name': self.mid_name,
            'num_copies': self.num_copies,
            'cemetery': self.cemetery,
            'month': self.month,
            'day': self.day,
            'years': self.years,
            'death_place': self.death_place,
            'age_of_death': self.age_of_death,
            'borough': self.borough,
            'letter': self.letter,
            'comment': self.comment,
            'suborder_number': self.suborder_number
        }
