"""
.. module:: constants.suborder_form.

    :synopsis: Defines constants used for the suborder form
    :This file will hold suborders field drop-down values
"""

MONTHS = [
    ("", "-- Select Month --"),
    ("01", "January"),
    ("02", "February"),
    ("03", "March"),
    ("04", "April"),
    ("05", "May"),
    ("06", "June"),
    ("07", "July"),
    ("08", "August"),
    ("08", "September"),
    ("10", "October"),
    ("11", "November"),
    ("12", "December")
]

GENDERS = [
    ("", "-- Select Gender --"),
    ("Male", "Male"),
    ("Female", "Female")
]

PHOTO_GALLERY_SIZES = [
    ("", "-- Select Size --"),
    ("8x10", "8x10"),
    ("11x14", "11x14"),
    ("16x20", "16x20")
]

TAX_PHOTO_SIZES = [
    ("", "-- Select Size --"),
    ("8x10", "8x10"),
    ("11x14", "11x14")
]

COLLECTIONS = [
    ("", "-- Select Collection --"),
    ('1940', '1940'),
    ('1980', '1980'),
    ('Both', 'Both')
]

ORDER_TYPES = [
    ("", "-- Select Order Type --"),
    ("birth_certificate_form", "Birth Certificate"),
    ("death_certificate_form", "Death Certificate"),
    ("marriage_certificate_form", "Marriage Certificate"),
    ("photo_gallery_form", "Photo Gallery"),
    ("tax_photo_form", "Tax Photo")
]

DELIVERY_METHODS = [
    ("", "-- Select Delivery Method --"),
    ("Mail", 'Mail'),
    ("Email", 'Email'),
    ("Pickup", 'Pickup')
]

ORDER_STATUS = [
    ("Received", 'Received'),
    ("Microfilm", 'Microfilm: When an order needs to be printed from the Microfilm'),
    ("Offsite", 'Offsite: Has to be ordered from Offsite to be fulfilled'),
    ("Processing", 'Processing: For photo orders only'),
    ("Not Found", 'Not Found: A Not Found letter was sent to the customer'),
    ("Undeliverable", 'Undeliverable: When an order is returned as undeliverable by USPS'),
    ("Refund", 'Refund: The order has been sent to Administration for a refund')
]

BOROUGHS = [
    ("", "-- Select Borough --"),
    ("Bronx", 'Bronx'),
    ("Manhattan", 'Manhattan'),
    ("Staten Island", 'Staten Island'),
    ("Brooklyn", 'Brooklyn'),
    ("Queens", 'Queens')
]
