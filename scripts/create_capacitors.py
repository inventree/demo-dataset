from inventree.api import InvenTreeAPI

from inventree.part import Part, PartCategory
from inventree.stock import StockItem, StockLocation
from inventree.company import SupplierPart

import random
import sys

INVENTREE_URL = "http://localhost:8000"
INVENTREE_USERNAME = "admin"
INVENTREE_PASSWORD = "inventree"

api = InvenTreeAPI(INVENTREE_URL, username=INVENTREE_USERNAME, password=INVENTREE_PASSWORD)

category = 6

packages = [
    '0402',
    '0603',
    '0805',
]

values = [
    # '100pF',
    '100nF',
    '1uF',
    '10uF',
]

for package in packages:
    for value in values:
        name = f"C_{value}_{package}"
        description = f"{value} in {package} SMD package"
        keywords = "cap smd ceramic"

        Part.create(api, data={
            'name': name,
            'category': category,
            'description': description,
            'keywords': keywords,
            'purchaseable': True,
        })
