"""
.. module:: constants.status.

    :synopsis: Defines constants used throughout the application
    :This file will hold the status of all of the orders
    :statuses 
    1. Received || Set to this by default
    2. Processing
       a)found
       b)printed
    3. Mailed/Pickup
    4. Not_Found
       a)Letter_generated
       b)Undeliverable - Cant move down the line
    5. Done - End of status changes
    
"""
RECEIVED = 'Received'
MICROFILM = 'Microfilm'
OFFSITE = 'Offsite'
PROCESSING = 'Processing'
NOT_FOUND = 'Not_Found'
UNDELIVERABLE = 'Undeliverable'
REFUND = 'Refund'
DONE = 'Done'
ALL = 'all'

DROPDOWN = [
    (ALL, "All"),
    (RECEIVED, 'Received'),
    (MICROFILM, 'Microfilm'),
    (OFFSITE, 'Offsite'),
    (PROCESSING, 'Processing'),
    (NOT_FOUND, 'Not Found'),
    (UNDELIVERABLE, 'Undeliverable'),
    (REFUND, 'Refund'),
    (DONE, 'Done'),
]

ORDER_STATUS_LIST = [
    (RECEIVED, 'Received'),
    (MICROFILM, 'Microfilm: When an order needs to be printed from the Microfilm'),
    (OFFSITE, 'Offsite: Has to be ordered from Offsite to be fulfilled'),
    (PROCESSING, 'Processing: For photo orders only'),
    (NOT_FOUND, 'Not Found: A Not Found letter was sent to the customer'),
    (UNDELIVERABLE, 'Undeliverable: When an order is returned as undeliverable by USPS'),
    (REFUND, 'Refund: The order has been sent to Administration for a refund'),
]
