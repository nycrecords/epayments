from datetime import timedelta
from flask import make_response, request, current_app, url_for
from functools import update_wrapper


def crossdomain(
        origin=None,
        methods=None,
        headers=None,
        max_age=21600,
        attach_to_all=True,
        automatic_options=True):
    """
    Allow requests to be submitted from alternate domains.
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None:
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))

            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def make_public_order(order):
    """
    Create a JSON object with URI that references a specific order.

    :param order: order as a JSON object
    :return: JSON object
    """
    new_order = {}
    for field in order:
        if field == 'SubOrderNo':
            new_order['uri'] = url_for(
                                        'get_order',
                                        order_id=order['SubOrderNo'],
                                        _external=True
                                        )
        else:
            new_order[field] = order[field]

    return new_order
