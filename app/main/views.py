import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, current_app, send_from_directory, flash, jsonify
from flask_login import login_user, current_user, logout_user
from app.main import main
from app.main.utils import allowed_file, import_xml
from app.import_utils import import_from_api
from app.models import Users
from app.main.forms import SearchOrderForm, NewOrderForm


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default route for the application."""
    if not current_user.is_authenticated:
        return redirect(url_for("main.newlogin"))
    return render_template('index.html', user=current_user.get_id(), form=SearchOrderForm())


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
    all_orders = json.get('all_orders')
    return jsonify(order_rows=render_template('order_table.html', orders=all_orders))


@main.route('/listinfo', methods=['POST'])
def listinfo():
    json = request.get_json(force=True)
    order_info = json.get('order_info')
    order_type = order_info['order_type']
    order_type_template_handler = {
        'Birth Search': 'birth_search.html',
        'Birth Cert': 'birth_cert.html',
        'Marriage Search': 'marriage_search.html',
        'Marriage Cert': 'marriage_cert.html',
        'Death Search': 'death_search.html',
        'Death Cert': 'death_cert.html',
        'Tax Photo': 'tax_photo.html',
        'Photo Gallery': 'photo_gallery.html',
        'Property Card': 'property_card.html',
        'OCME': 'ocme.html',
        'HVR': 'hvr.html',
        'No Amends': 'no_amends.html'
    }
    return jsonify(info_tab=render_template('orders/{}'.format(order_type_template_handler[order_type]),
                               order_info=order_info))


@main.route('/listhistory', methods=['POST'])
def listhistory():
    json = request.get_json(force=True)
    return jsonify(history_tab=render_template('history_row.html', history=json['history']))


@main.route('/newOrder', methods=['GET'])
def newOrder():
    return render_template('order_forms/new_order_form.html', form=NewOrderForm())


@main.route('/newSuborderForm', methods=['POST'])
def newSuborderForm():
    json = request.get_json(force=True)
    return jsonify(suborder_form=render_template('order_forms/new_suborder_form.html', num=json['suborder_count']))


@main.route('/newSuborder', methods=['POST'])
def newSuborder():
    json = request.get_json(force=True)
    order_type = json['order_type']
    suborder_count = json['suborder_count']

    template_handler = {
        'Birth Cert': 'birth_cert_form.html',
        'Death Cert': 'death_cert_form.html',
        'Marriage Cert': 'marriage_cert_form.html',
        'Photo Gallery': 'photo_gallery_form.html',
        'Tax Photo': 'tax_photo_form.html'
    }
    template = 'order_forms/{}'.format(template_handler[order_type])
    return jsonify(template=render_template(template, num=suborder_count))