"""
This script finds stock items which are not associated with a SupplierPart, and:

- Adds a SupplierPart Reference
- Adds a PurchasePrice reference
"""

from random import randint

from progress.bar import Bar

from inventree.api import InvenTreeAPI

from inventree.company import SupplierPart, SupplierPriceBreak
from inventree.part import Part
from inventree.stock import StockItem

api = InvenTreeAPI("http://localhost:8000", username="admin", password="inventree")

# ID for the "passives" category
passives_category_id = 4

location = 11

parts = Part.list(api, category=passives_category_id, cascade=True)

bar = Bar('Updating Stock Records', max=len(parts))

for part in parts:

    supplier_parts = SupplierPart.list(api, part=part.pk)

    for sp in supplier_parts:

        # Find any supplier parts without stock
        stock_items = StockItem.list(api, part=part.pk, supplier_part=sp.pk)

        # Ignore if there are existing stock items
        if len(stock_items) > 0:
            continue

        quantity = randint(0, 100)

        if quantity <= 25:
            continue

        price_breaks = SupplierPriceBreak.list(api, part=sp.pk)

        pp = None
        ppc = None


        for pb in price_breaks:
            if pb.quantity == 1:
                pp = pb.price
                ppc = pb.price_currency

        # Create a new StockItem
        StockItem.create(
            api,
            {
                'part': part.pk,
                'supplier_part': sp.pk,
                'quantity': quantity,
                'location': location,
                'packaging': 'cut tape',
                'purchase_price': pp,
                'purchase_price_currency': ppc,
            }
        )

    bar.next()

bar.finish()
