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
        'order_rows': ''
    }

    all_orders = json.get('all_orders')
    data['order_rows'] = render_template('order_table.html',
                                          orders=all_orders)
    return jsonify(data)


@main.route('/listinfo', methods=['POST'])
def listinfo():
    json = request.get_json(force=True)
    data = {
        'info_tab': ''
    }

    order_info = json.get('order_info')
    order_type = order_info['order_type']
    match order_type:
        case 'Birth Search':
            info_tab = render_template('orders/birth_search.html', order_info=order_info)
        case 'Birth Cert':
            info_tab = render_template('orders/birth_cert.html', order_info=order_info)
        case 'Marriage Search':
            info_tab = render_template('orders/marriage_search.html', order_info=order_info)
        case 'Marriage Cert':
            info_tab = render_template('orders/marriage_cert.html', order_info=order_info)
        case 'Death Search':
            info_tab = render_template('orders/death_search.html', order_info=order_info)
        case 'Death Cert':
            info_tab = render_template('orders/death_cert.html', order_info=order_info)
        case 'Tax Photo':
            info_tab = render_template('orders/tax_photo.html', order_info=order_info)
        case 'Photo Gallery':
            info_tab = render_template('orders/photo_gallery.html', order_info=order_info)
        case 'Property Card':
            info_tab = render_template('orders/property_card.html', order_info=order_info)
        case 'OCME':
            info_tab = render_template('orders/ocme.html', order_info=order_info)
        case 'HVR':
            info_tab = render_template('orders/HVR.html', order_info=order_info)

    data['info_tab'] = info_tab
    return jsonify(data)


@main.route('/listhistory', methods=['POST'])
def listhistory():
    json = request.get_json(force=True)
    data = {'history_tab': render_template('history_row.html', history=json['history'])}
    return jsonify(data)
