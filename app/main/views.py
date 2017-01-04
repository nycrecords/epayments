from flask import render_template, request, make_response, jsonify
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    """Default route for the application."""
    # if request.method == 'POST':
    #     print 1
    # print request.form['submit']
    #     if request.form['submit'] == 'Print':
    #         order_number = str(request.form["order_number"])
    #         print order_number
    return render_template('index.html')


@main.route('/printorders', methods=['GET', 'POST'])
def printorders():
    """Printing page for orders from application."""
    # TODO: Filter orders for printing into an array
    orderfilters = request.json
    print(orderfilters)
    return render_template('printorders.html')


@main.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@main.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
