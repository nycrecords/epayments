"""
.. module:: constants.print_type.

    :synopsis: Defines constants for Order Types
"""

BIRTH_SEARCH = "Birth Search"
BIRTH_CERT = "Birth Cert"
MARRIAGE_SEARCH = "Marriage Search"
MARRIAGE_CERT = "Marriage Cert"
DEATH_SEARCH = "Death Search"
DEATH_CERT = "Death Cert"
NO_AMENDS = "No Amends"
TAX_PHOTO = "Tax Photo"
PHOTO_GALLERY = "Photo Gallery"
PROPERTY_CARD = "Property Card"
OCME = "OCME"
HVR = "HVR"
PHOTOS = 'photos'
VITAL_RECORDS = 'vital_records'
ALL = 'all'

VITAL_RECORDS_LIST = [
    BIRTH_CERT,
    BIRTH_SEARCH,
    MARRIAGE_CERT,
    MARRIAGE_SEARCH,
    DEATH_CERT,
    DEATH_SEARCH,
    PROPERTY_CARD
]

PHOTOS_LIST = [
    TAX_PHOTO,
    PHOTO_GALLERY
]


CLIENT_ID_DICT = {
    "10000102": "Birth Search",
    "10000147": "Birth Cert",
    "10000104": "Marriage Search",
    "10000181": "Marriage Cert",
    "10000103": "Death Search",
    "10000182": "Death Cert",
    "10000106": "No Amends",
    "10000048": "Tax Photo",
    "10000060": "Photo Gallery",
    "10000110": "Property Card",
    "10000120": "OCME",
    "10000107": "HVR",
}


DROPDOWN = [
    (ALL, "All"),
    (BIRTH_SEARCH, "Birth Search"),
    (BIRTH_CERT, "Birth Cert"),
    (MARRIAGE_SEARCH, "Marriage Search"),
    (MARRIAGE_CERT, "Marriage Cert"),
    (DEATH_SEARCH, "Death Search"),
    (DEATH_CERT, "Death Cert"),
    (NO_AMENDS, "No Amends"),
    (TAX_PHOTO, "Tax Photo"),
    (PHOTO_GALLERY, "Photo Gallery"),
    (PROPERTY_CARD, "Property Card"),
    (OCME, "OCME"),
    (HVR, "HVR"),
    (PHOTOS, 'Photos'),
    (VITAL_RECORDS, 'Vital Records')
]
