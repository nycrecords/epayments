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
TAX_PHOTO = "Tax Photo"
PHOTO_GALLERY = "Photo Gallery"
PROPERTY_CARD = "Property Card"

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
    "10000048": "Tax Photo",
    "10000060": "Photo Gallery",
    "10000058": "Property Card"
}
