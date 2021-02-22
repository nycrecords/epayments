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

# FOUND = 'Found'
# PRINTED = 'Printed'
# MAILED_PICKUP = 'Mailed/Pickup'
# EMAILED = 'Emailed'
# LETTER_GENERATED = 'Letter_Generated'
# REFUNDED = 'Refunded'
