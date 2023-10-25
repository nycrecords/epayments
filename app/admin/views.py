from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.admin import admin
from app.admin.utils import assign_user_role
from app.constants.role import ROLES
from app.models import Users


@admin.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.is_admin:
        flash("Insufficient privileges to view this page.")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        user = request.form.get('user')
        role = request.form.get('role')
        assign_user_role(user, role)

    users = Users.query.all()

    return render_template('admin/index.html', user_list=users, roles=ROLES)
