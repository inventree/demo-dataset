"""
This script adds new supplier data and supplier pricing for the demo dataset.

The supplier part numbers here are not real, neither is the pricing.
None of this data should be used for anything in the realm of sensible decision making.
"""

import random
import string

from progress.bar import Bar

from inventree.api import InvenTreeAPI

from inventree.company import Company, SupplierPart, SupplierPriceBreak
from inventree.part import Part

api = InvenTreeAPI("http://localhost:8000", username="admin", password="inventree")

# ID for the "passives" category
passives_category_id = 4

# List of electronics suppliers we wish to create supplier parts for
supplier_ids = [
    1,   # DigiKey
    2,   # Mouser
    3,   # Arrow
    39,  # LCSC
    40,  # Newark
    41,  # Future Electronics
]

# Special currency (default = USD)
currencies = {
    2: 'AUD',  # Mouser
    39: 'CNY',  # LCSC
    41: 'CAD', # Future
}

parts = Part.list(api, category=passives_category_id, cascade=True)

bar = Bar('Creating Supplier Part Data', max=len(parts))

for part in parts:
    
    bar.next()

    # Create at least one supplier part for each supplier
    for supplier_id in supplier_ids:
        supplier_parts = SupplierPart.list(
            api,
            part=part.pk,
            supplier=supplier_id,
        )

        # Supplier part already exists for this supplier
        if len(supplier_parts) > 0:
            continue

        supplier = Company(api, pk=supplier_id)

        # Create a new supplier part for this supplier
        SKU = supplier.name.upper()[0:3]

        SKU += "-" + "".join(random.choice(string.digits) for _ in range(5))
        SKU += "-"
        SKU += "".join(random.choice(string.ascii_uppercase) for _ in range(3))

        # Create a new supplier part based on randomly generated SKU
        SupplierPart.create(
            api,
            {
                "part": part.pk,
                "supplier": supplier.pk,
                "SKU": SKU,
            }
        )

    # Now, ensure that each SupplierPart has some associated price break information
    supplier_parts = SupplierPart.list(api, part=part.pk)

    for sp in supplier_parts:
        price_breaks = SupplierPriceBreak.list(api, part=sp.pk)

        # Skip for any supplier pars which already have price-break information
        if len(price_breaks) > 0:
            continue

        currency = currencies.get(sp.supplier, 'USD')

        # Start with the highest price break for 1000x
        pb_1000 = 0.0025 + random.random() * 0.025
        pb_100 = pb_1000 * (10 + random.random() * 1.25)
        pb_1 = pb_100 * (10 + random.random() * 2.5)

        SupplierPriceBreak.create(
            api,
            {
                "part": sp.pk,
                "quantity": 1,
                "price": round(pb_1, 4),
                "price_currency": currency
            }
        )

        SupplierPriceBreak.create(
            api,
            {
                "part": sp.pk,
                "quantity": 100,
                "price": round(pb_100, 4),
                "price_currency": currency
            }
        )

        SupplierPriceBreak.create(
            api,
            {
                "part": sp.pk,
                "quantity": 1000,
                "price": round(pb_1000, 4),
                "price_currency": currency
            }
        )


bar.finish()