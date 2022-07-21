import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, current_app, send_from_directory, flash, jsonify
from flask_login import login_user, current_user, logout_user
from app.main import main
from app.main.utils import allowed_file, import_xml
from app.import_utils import import_from_api
from app.models import Users
from app.main.forms import SearchOrderForm


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default route for the application."""
    if not current_user.is_authenticated:
        return redirect(url_for("main.newlogin"))
    form = SearchOrderForm()
    return render_template('index.html', form=form)


@main.route('/import', methods=['GET', 'POST'])
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


# noinspection PyTypeChecker,PyTypeChecker
@main.route('/static/files/<string:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(current_app.config["PRINT_FILE_PATH"], filename, as_attachment=True)


@main.route('/newlogin', methods=['GET'])
def newlogin():
    """ Initial load in the login page """
    return render_template('newlogin.html')


@main.route('/newlogin', methods=['POST'])
def newloginAuth():
    """
    Authenticates the user and logs in the user

    email: request email
    password: request password

    Returns: redirects to ePayments page on successful authorization
    if form fields are missing, an error will be displayed
    """

    email = request.form['email']
    password = request.form['password']

    user = Users.query.filter_by(email=email).one_or_none()
    if user is None:
        error = 'Invalid Email'
        flash(error, 'danger')
    else:
        valid_password = user.verify_password(password)
        if not valid_password:
            error = 'Invalid Password'
            flash(error, 'danger')
        else:
            login_user(user)
            return redirect(url_for('main.index'))

    return render_template('newlogin.html')


@main.route('/newlogout')
def newlogout():
    logout_user()
    flash('Logout Successful', 'success')
    return redirect(url_for('main.index'))


@main.route('/listorders', methods=['GET', 'POST'])
def listorders():
    json = request.get_json(force=True)
    data = {
        'order_table': ''
    }

    all_orders = json.get('all_orders')
    order_count = json.get('order_count')
    suborder_count = json.get('suborder_count')
    data['order_table'] = render_template('order_table.html',
                                          orders=all_orders,
                                          order_count=order_count,
                                          suborder_count=suborder_count)
    return jsonify(data)

# @main.route('/search-orders', methods=['GET'])
# def search_orders():
#     form = SearchOrderForm()
#
#     # set form data
#     form.order_number.data = request.args.get('order_number', '')
#     form.suborder_number.data = request.args.get('suborder_number')
#     form.delivery_method.data = request.args.get('delivery_method', '')
#     form.status.data = request.args.get('status', '')
#     form.billing_name.data = request.args.get('billing_name', '')
#
#     return render_template('index.html', form=form)
