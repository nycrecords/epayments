import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, current_app, send_from_directory, flash, jsonify
from flask_login import login_user, current_user, logout_user

from app.constants import status, order_type
from app.import_utils import import_from_api
from app.main import main
from app.main.forms import (SearchOrderForm, MainOrderForm, SuborderForm, BirthCertificateOrderForm,
                            DeathCertificateOrderForm,
                            MarriageCertificateOrderForm, PhotoGalleryOrderForm, TaxPhotoOrderForm)
from app.main.utils import allowed_file, import_xml
from app.models import Users


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default route for the application."""
    if not current_user.is_authenticated:
        return redirect(url_for("main.login"))
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


@main.route('/login', methods=['GET', 'POST'])
def login():
    """ Initial load in the login page """
    if request.method == 'POST':
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
    return render_template('login.html')


@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('Logout Successful', 'success')
    return redirect(url_for('main.index'))


@main.route('/order', methods=['GET', 'POST'])
def order():
    main_order_form = MainOrderForm()
    suborders = SuborderForm()
    if request.method == "POST":
        return main_order_form.data
    return render_template('order_forms/main_order_form.html',
                           form=main_order_form,
                           suborders=suborders)


@main.route('/newSuborderForm', methods=['POST'])
def newSuborderForm():
    json = request.get_json(force=True)
    return jsonify(suborder_form=render_template('order_forms/suborder_form_.html',
                                                 num=json['suborder_count'],
                                                 form=SuborderForm()))


@main.route('/suborder_form', methods=['POST'])
def suborder_form():
    json = request.get_json(force=True)
    return render_template('order_forms/suborder_form.html', status=status.ORDER_STATUS_LIST,
                           order_types=order_type.ORDER_TYPES_LIST,
                           suborder_count=json["suborder_count"])


@main.route('/newSuborder', methods=['POST'])
def newSuborder():
    json = request.get_json(force=True)
    order_type = json['order_type']
    suborder_count = json['suborder_count']

    template_handler = {
        'Birth Cert': ('birth_cert_form.html', BirthCertificateOrderForm()),
        'Death Cert': ('death_cert_form.html', DeathCertificateOrderForm()),
        'Marriage Cert': ('marriage_cert_form.html', MarriageCertificateOrderForm()),
        'Photo Gallery': ('photo_gallery_form.html', PhotoGalleryOrderForm()),
        'Tax Photo': ('tax_photo_form.html', TaxPhotoOrderForm())
    }
    template = 'order_forms/{}'.format(template_handler[order_type][0])
    form = template_handler[order_type][1]
    return jsonify(template=render_template(template, num=suborder_count, form=form))
