"""
This script adds supplier availability data to some SupplierPart objects
"""

from random import randint
from matplotlib.style import available

from progress.bar import Bar

from inventree.api import InvenTreeAPI

from inventree.company import SupplierPart
from inventree.part import Part
from inventree.stock import StockItem
from scipy import rand

api = InvenTreeAPI("http://localhost:8000", username="admin", password="inventree")

# ID for the "passives" category
passives_category_id = 4

parts = Part.list(api, category=passives_category_id, cascade=True)

bar = Bar('Updating Supplier Availability', max=len(parts))

for part in parts:

    supplier_parts = SupplierPart.list(api, part=part.pk)

    for sp in supplier_parts:

        # Do not update every SupplierPart instance
        if randint(0, 10) > 3:
            continue

        available = randint(500, 50000)

        sp.save(
            data={
                'available': available
            }
        )

    bar.next()

bar.finish()
