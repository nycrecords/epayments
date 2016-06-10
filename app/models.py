from . import db

class Order(db.Model):
    """
    Define the Order class with the following columns and relationships:


    """
    __tablename__ = 'order'
    orderno = db.Column(db.Integer)
    clientagencyname = db.Column(db.String(64))
    shiptoname = db.Column(db.String(64))
    shiptostreetadd = db.Column(db.String(64))
    shiptostreetadd2 = db.Column(db.String(64))
    shiptocity = db.Column(db.String(64))
    shiptostate = db.Column(db.String(64))
    shiptozipcode = db.Column(db.Integer)
    shiptocountry = db.Column(db.String(64))
    shiptophone = db.Column(db.String(64))
    customeremail = db.Column(db.String(64))
    shippinginstructions = db.Column(db.String(64))
    clientsdata = db.Column(db.Text)
    confirmationmessage = db.Column(db.Text)
    datereceived = db.Column(db.DateTime)
    billingname = db.Column(db.String(64))
    datelastmodified = db.Column(db.DateTime)
    suborderno = db.Column(db.Integer, primary_key=True)
    clientid = db.Column(db.Integer)
