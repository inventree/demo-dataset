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

capacitors = Part.list(api, category=6)

storage = StockLocation(api, pk=8)

count = 0

for cap in capacitors:

    if random.random() > 0.65:
        continue

    # Get the first matching supplierpart
    sp_list = SupplierPart.list(api, part=cap.pk)

    for sp in sp_list:
        if random.random() > 0.6:
            continue

        status = 10

        q = random.random()

        quantity = 1000

        if q < 0.1:
            quantity = 500

        elif q > 0.85:
            quantity = 4000

        if random.random() < 0.2:
            quantity += int(random.random() * 2000)

        if random.random() > 0.95:
            status = 55  # Damaged
        elif random.random() > 0.95:
            status = 50  # Attention

        StockItem.create(api, data={
            'location': storage.pk,
            'part': cap.pk,
            'quantity': quantity,
            'supplier_part': sp.pk,
            'packaging': 'reel',
            'status': status,
        })

        count += 1

print(f"Created {count} new stock items")
    
    
