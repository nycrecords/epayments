import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, current_app, flash, session
from flask_login import current_user, login_required

from app import login_manager
from app.api.v1.utils import create_new_order
from app.constants.suborder_form import ORDER_TYPES
from app.import_utils import import_from_api
from app.main import main
from app.main.forms import SearchOrderForm, MainOrderForm
from app.main.utils import allowed_file, import_xml
from app.models import Users


@login_manager.user_loader
def user_loader(guid: str) -> Users:
    user = Users.query.filter_by(guid=guid).one_or_none()
    if user.session_id == session.sid:
        return user


@main.route('/health', methods=['GET'])
def health():
    return ''


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_authenticated:
        duplicate_session = request.args.get('duplicate_session')
        return render_template(
            'index.html',
            user=current_user.get_id(),
            duplicate_session=duplicate_session,
            form=SearchOrderForm()
        )
    return redirect(url_for('auth.login'))


@main.route('/import', methods=['GET', 'POST'])
@login_required
def import_tar():
    """Import Orders into the database from the tar file."""
    if request.method == 'POST':
        file_ = request.files['file']
        if file_ and allowed_file(file_.filename):
            actual_filename = 'DOR-{date}.tar'.format(date=datetime.now().strftime('%Y-%m-%d'))
            filename = os.path.join(current_app.config['LOCAL_FILE_PATH'], actual_filename)
            file_.save(filename)
            import_xml(filename)
            return redirect(url_for('main.index'))

        start_date = request.form["start-date"]
        end_date = request.form["end-date"]
        if start_date and end_date:
            import_from_api(start_date, end_date)
    return render_template('main/import.html')


@main.route('/new_order', methods=['GET', 'POST'])
@login_required
def new_order():
    form = MainOrderForm()
    if request.method == "POST":
        # Validate form fields. This is checked first to avoid nested ifs
        if not form.validate_on_submit():
            flash('Not all required fields have been entered correctly. Please correct the fields in red below.',
                  'error')
        # Ensure suborder exists in form before saving new order
        elif len(form.suborders) < 1:
            flash('Suborder required to place order.', 'error')
        else:
            # Create order and save to db
            order = create_new_order(form.data)
            flash(f'Order#: {order} submitted successfully.', 'success')
            return redirect(url_for('main.new_order'))
    return render_template('order_forms/new_order_form.html', form=form, order_types=ORDER_TYPES)


@main.route('/suborder_form', methods=['POST'])
def suborder_form():
    form = MainOrderForm()
    order_type = request.form['order-type']

    # Append a new suborder to MainOrderForm
    suborder = form.suborders.append_entry()

    # Append a new FieldList of order_type to the suborder
    suborder[order_type].append_entry()

    return render_template('order_forms/suborder_form.html', form=form)


@main.route('/active', methods=['POST'])
def active():
    """
    Extends a user's session.
    :return:
    """
    session.modified = True
    return 'OK'
