CLIENT_AGENCY_NAMES = {
    "10000048": "Photo Tax",
    "10000060": "Photo Gallery",
    "10000102": "Birth Search",
    "10000147": "Birth Cert",
    "10000104": "Marriage Search",
    "10000181": "Marriage Cert",
    "10000103": "Death Search",
    "10000182": "Death Cert"
}

ORDER_TYPES = [
    'tax photo',
    'online gallery',
    'Birth search',
    'Birth cert',
    'Marriage search',
    'Marriage cert',
    'Death search',
    'Death cert'
]

VITAL_RECORDS_ORDERS = {
    'Birth search',
    'Birth cert',
    'Marriage search',
    'Marriage cert',
    'Death search',
    'Death cert'
}

PHOTO_ORDERS = {
    'tax photo',
    'online gallery'
}

MULTIPLE_ORDERS = [
    'All',
    'multipleitems',
    'vitalrecordsphotos'
]

MULTIPLE_ITEMS_IN_CART = 'multipleitems'

VITAL_RECORDS_PHOTOS_ORDER = 'vitalrecordsphotos'

ALLOWED_EXTENSIONS = frozenset(['tar', 'xml'])