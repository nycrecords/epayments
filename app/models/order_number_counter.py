from app import db


class OrderNumberCounter(db.Model):
    """
    Define the new Orders class with the following Columns & relationships
    """
    __tablename__ = 'order_number_counter'
    year = db.Column(db.Integer(), primary_key=True, nullable=False)
    _next_order_number = db.Column(db.Integer(), db.Sequence('order_seq'), name='next_order_number')



    @property
    def next_order_number(self):
        from app.db_utils import update_object
        num = self._next_order_number
        update_object(
            {'_next_order_number': self._next_order_number + 1},
            OrderNumberCounter,
            self.year
        )
        return num


