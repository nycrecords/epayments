# This file will hold the status of all of the orders

"""
.. module:: _constants_.status.

    :synopsis: Defines _constants_ used throughout the application
"""
# statuses = {
#    1. Received || Set to this by default
#    2. Processing
#        a)found
#        b)printed
#    3. Mailed/Pickup
#    4. Not_Found
#        a)Letter_generated
#        b)Undeliverable - Cant move down the line
#    5. Done - End of status changes
#    }

RECEIVED = 'Received'
PROCESSING = 'Processing'
FOUND = 'Found'
PRINTED = 'Printed'
MAILED_PICKUP = 'Mailed/Pickup'
NOT_FOUND = 'Not_Found'
LETTER_GENERATED = 'Letter_Generated'
UNDELIVERABLE = 'Undeliverable'
DONE = 'Done'

