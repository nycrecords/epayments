import os
from datetime import datetime

from flask import render_template, redirect, url_for, request, current_app, send_from_directory, flash
from flask_login import login_user, current_user, logout_user

from app.import_utils import import_from_api
from app.main import main
from app.main.forms import SearchOrderForm, MainOrderForm, SignInForm
from app.main.utils import allowed_file, import_xml
from app.models import Users
from app.constants import form_choices


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
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SignInForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.username.data).first()
        password = form.password.data
        if user is None:
            flash('Invalid Email Address')
        else:
            valid_password = user.verify_password(password)
            if not valid_password:
                flash('Invalid Password')
            else:
                login_user(user)
                return redirect(url_for('main.index'))
    return render_template('login.html', form=form)


@main.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('Logout Successful', 'success')
    return redirect(url_for('main.index'))


@main.route('/new_order', methods=['GET', 'POST'])
def new_order():
    form = MainOrderForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if len(form.suborders) < 1:
                flash("Suborder required to place order.")
            else:
                return form.data
    return render_template('order_forms/new_order_form.html', form=form, order_types=form_choices.ORDER_TYPES)


@main.route("/suborder_form", methods=["POST"])
def suborder_form():
    form = MainOrderForm()
    order_type = request.form['order-type']

    # Append a new suborders (FieldList) to MainOrderForm
    suborder = getattr(form, 'suborders').append_entry()
    # Get index of appended suborders
    idx = int(suborder.id.replace('suborders-', ''))
    # Append a new FieldList of order_type to suborders
    form.suborders[-1][order_type].append_entry()

    return render_template('order_forms/suborder_form.html', form=form)
