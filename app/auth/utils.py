from datetime import datetime

from flask import current_app, session, redirect, url_for, request, render_template, flash
from flask_login import login_user, current_user

from app import db
from app.constants import auth_event_type
from app.db_utils import create_object, update_object
from app.lib.onelogin.saml2.auth import OneLogin_Saml2_Auth
from app.lib.onelogin.saml2.utils import OneLogin_Saml2_Utils
from app.models import Users
from app.models.auth_events import AuthEvents


def init_saml_auth(onelogin_request):
    saml_sp = OneLogin_Saml2_Auth(onelogin_request, custom_base_path=current_app.config['SAML_PATH'])
    return saml_sp


def prepare_onelogin_request(flask_request):
    return {
        'https': 'on' if flask_request.scheme == 'https' else 'off',
        'http_host': flask_request.host,
        'script_name': flask_request.path,
        'get_data': flask_request.args.copy(),
        'post_data': flask_request.form.copy()
    }


def saml_sso(saml_sp):
    # Generate the SAML SSO login request and redirect the user to the IdP login page
    return redirect(saml_sp.login(url_for('main.index', _external=True, _scheme='https')))


def saml_slo(saml_sp):
    name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
    if 'samlNameId' in session:
        name_id = session['samlNameId']
    if 'samlSessionIndex' in session:
        session_index = session['samlSessionIndex']
    if 'samlNameIdFormat' in session:
        name_id_format = session['samlNameIdFormat']
    if 'samlNameIdNameQualifier' in session:
        name_id_nq = session['samlNameIdNameQualifier']
    if 'samlNameIdSPNameQualifier' in session:
        name_id_spnq = session['samlNameIdSPNameQualifier']
    if request.args.get('timeout'):
        session['timeout'] = request.args.get('timeout')
    return saml_sp.logout(name_id=name_id, session_index=session_index, nq=name_id_nq, name_id_format=name_id_format,
                          spnq=name_id_spnq)


def saml_acs(saml_sp, onelogin_request):
    request_id = None
    if 'AuthNRequestID' in session:
        request_id = session['AuthNRequestID']
    saml_sp.process_response(request_id=request_id)
    errors = saml_sp.get_errors()

    if not errors:
        session.pop('AuthNRequestID', None)
        session['samlUserdata'] = saml_sp.get_attributes()
        session['samlNameId'] = saml_sp.get_nameid()
        session['samlNameIdFormat'] = saml_sp.get_nameid_format()
        session['samlNameIdNameQualifier'] = saml_sp.get_nameid_nq()
        session['samlNameIdSPNameQualifier'] = saml_sp.get_nameid_spnq()
        session['samlSessionIndex'] = saml_sp.get_session_index()
        self_url = OneLogin_Saml2_Utils.get_self_url(onelogin_request)
        user_data = {key: value_list[0] if value_list else None for key, value_list in session['samlUserdata'].items()}
        user = _process_user_data(user_data)

        if user:
            if user.agency_user:
                login_user(user)
                duplicate_session = user.session_id is not None

                if duplicate_session:
                    log_duplicate_session(user.guid)

                update_object(
                    {'session_id': session.sid, 'last_sign_in_at': datetime.utcnow()},
                    Users,
                    current_user.guid
                )
                create_auth_event(user.guid, auth_event_type.USER_LOGIN, {'success': True})
            else:
                create_auth_event(user_data.get('GUID'), auth_event_type.USER_FAILED_LOG_IN,
                                  {'User Data': user_data, 'message': 'Awaiting agency approval.', 'success': False})
                return render_template('contact_us.html')
        else:
            flash(
                'Sorry, we couldn\'t find your account. Please send an email to appsupport@records.nyc.gov for assistance.',
                category='danger')
            return redirect(url_for('main.index'))

        if 'RelayState' in request.form and self_url != request.form['RelayState']:
            # To avoid 'Open Redirect' attacks, before execute the redirection confirm
            # the value of the request.form['RelayState'] is a trusted URL.
            if duplicate_session:
                return redirect(saml_sp.redirect_to(request.form['RelayState'], {'duplicate_session': 'true'}))
            return redirect(request.form['RelayState'])
        return redirect(url_for('main.index'))
    else:
        flash("Oops! Something went wrong. Please try to perform your action again later.", category="warning")
        return redirect(url_for('main.index'))


def saml_sls(saml_sp):
    request_id = None
    if 'LogoutRequestID' in session:
        request_id = session['LogoutRequestID']
    dscb = lambda: session.clear()
    url = saml_sp.process_slo(keep_local_session=True, request_id=request_id, delete_session_cb=dscb)
    errors = saml_sp.get_errors()
    error_message = f"Errors on SAML Logout: {errors}" if len(errors) > 0 else None
    return redirect(url) if url else redirect(url_for('auth.logout', error_message=error_message))


def _process_user_data(user_data: dict):
    user_attributes = {
        'guid': user_data.get('GUID'),
        'email': user_data.get('mail'),
        'first_name': user_data.get('givenName'),
        'middle_initial': user_data.get('middle_name'),
        'last_name': user_data.get('sn'),
        'email_validated': user_data.get('nycExtEmailValidationFlag') == 'true'
    }

    username, domain = user_attributes['email'].split('@')

    if domain == 'records.nyc.gov':
        user = Users.query.filter_by(guid=user_attributes['guid']).first() or Users.query.filter_by(
            email=user_attributes['email']).first()
        if user:
            _update_user_data(user, user_attributes)
        else:
            user = _create_agency_user(Users(**user_attributes))
        return user


def _create_agency_user(user):
    user.last_sign_in_at = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    create_auth_event(user.guid, auth_event_type.USER_CREATED, {'success': True})
    return user


def _update_user_data(user: Users, user_attributes: dict):
    # Check if any attributes have changed
    if any(getattr(user, attr) != value for attr, value in user_attributes.items()):
        # Update user attributes
        for attr, value in user_attributes.items():
            setattr(user, attr, value)
        user.updated_at = datetime.utcnow()
        db.session.commit()
    return user


def create_auth_event(user_guid: str, auth_event_type: str, new_value: dict, previous_value=None):
    event = AuthEvents(
        user_guid=user_guid,
        type_=auth_event_type,
        timestamp=datetime.utcnow(),
        previous_value=previous_value,
        new_value=new_value
    )
    create_object(event)


def log_duplicate_session(user_guid: str):
    create_auth_event(user_guid, auth_event_type.USER_LOGGED_OUT, {'success': True, 'errors': 'duplicate_session'})
