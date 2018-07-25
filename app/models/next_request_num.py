from app import db


class NextOrder(db.Model):


    """
    Define the new Orders class with the following Columns & relationships



    """
    __table__='next_order_num'
    year = db.Column(db.Integer(), primary_key=True, nullable=False)
    next_request_num = db.Column(db.Integer(), db.Sequence('order_seq'), name='next_order_number')

    @property
    def next_order_number(self):
        from app.db_utils import update_object
        num = self._next_request_number
        update_object(
            {'_next_request_number': self._next_request_number + 1},
            NextOrder,
            self.year
        )
        return num


