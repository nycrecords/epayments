from . import db

# db.Model.metadata.reflect(db.engine)

class Order(db.Model):
    """
    Define the Order class with the following columns and relationships:

    orderno -- Column: String(64)
    clientagencyname -- Column: String(64)
    shiptoname -- Column: String(64)
    shiptostreetadd -- Column: String(64)
    shiptostreetadd2 -- Column: String(64)
    shiptocity  -- Column: String(64)
    shiptostate -- Column: String(64)
    shiptozipcode -- Column: String(64)
    shiptocountry -- Column: String(64)
    shiptophone -- Column: String(64)
    customeremail -- Column: String(64)
    shippinginstructions -- Column: String(64)
    clientsdata -- Column: Text
    confirmationmessage -- Column: Text
    datereceived -- Column: DateTime
    billingname -- Column: String(64)
    datelastmodified -- Column: DateTime
    suborderno -- Column: BigInteger, PrimaryKey
    clientid -- Column: Integer
    ordertypes -- Column: String(256)
    """
    __tablename__ = 'order'
    orderno = db.Column(db.String(64))
    clientagencyname = db.Column(db.String(64))
    shiptoname = db.Column(db.String(64))
    shiptostreetadd = db.Column(db.String(64))
    shiptostreetadd2 = db.Column(db.String(64))
    shiptocity = db.Column(db.String(64))
    shiptostate = db.Column(db.String(64))
    shiptozipcode = db.Column(db.String(64))
    shiptocountry = db.Column(db.String(64))
    shiptophone = db.Column(db.String(64))
    customeremail = db.Column(db.String(64))
    shippinginstructions = db.Column(db.String(64))
    clientsdata = db.Column(db.Text)
    confirmationmessage = db.Column(db.Text)
    datereceived = db.Column(db.DateTime)
    billingname = db.Column(db.String(64))
    datelastmodified = db.Column(db.DateTime)
    suborderno = db.Column(db.BigInteger, primary_key=True)
    clientid = db.Column(db.Integer)
    ordertypes = db.Column(db.String(256))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'orderno' : self.orderno,
            'clientagencyname' : self.clientagencyname,
            'shiptoname' : self.shiptoname,
            'shiptostreetadd' : self.shiptostreetadd,
            'shiptostreetadd2' : self.shiptostreetadd2,
            'shiptocity' : self.shiptocity,
            'shiptostate' : self.shiptostate,
            'shiptozipcode' : self.shiptozipcode,
            'shiptocountry' : self.shiptocountry,
            'shiptophone' : self.shiptophone,
            'customeremail' : self.customeremail,
            'shippinginstructions' : self.shippinginstructions,
            'clientsdata' : self.clientsdata,
            'confirmationmessage' : self.confirmationmessage,
            'datereceived' : str(self.datereceived),
            'billingname' : self.billingname,
            'datelastmodified' : self.datelastmodified,
            'suborderno' : self.suborderno,
            'clientid' : self.clientid,
            'ordertypes' : self.ordertypes
       }
