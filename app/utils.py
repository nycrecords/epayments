from flask import url_for


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
                                        'api_1_0.get_order',
                                        order_id=order['SubOrderNo'],
                                        _external=True
                                        )
        else:
            new_order[field] = order[field]

    return new_order
