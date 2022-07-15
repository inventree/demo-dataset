
from random import randint

from inventree.api import InvenTreeAPI

from inventree.part import Part, Parameter, ParameterTemplate
from inventree.stock import StockItem

api = InvenTreeAPI("http://localhost:8000", username="admin", password="inventree")

# Pin headers category
cat_id = 21

# Storage location
loc_id = 10

rows = [1, 2]
pitch = [1.27, 2.0, 2.54]
ways = range(2, 11)

# Parameter templates
templates = {}

for tmp in ParameterTemplate.list(api):
    templates[tmp.name] = tmp.pk

for r in rows:
    for p in pitch:
        for w in ways:

            n = r * w

            name = f"PinHeader_{r}x{w:02d}x{p}mm"
            description = f"Male pin header connector, {r} rows, {n} positions, {p}mm pitch, vertical"
            keywords = "pin header connector"

            # Check if this part already exists
            results = Part.list(api, search=name)

            if len(results) > 0:
                part = results[0]
            else:
                part = Part.create(
                    api,
                    {
                        'name': name,
                        'description': description,
                        'keywords': keywords,
                        'category': cat_id,
                        'purchaseable': True,
                        'component': True,
                    }
                )

            # Create stock item for this item
            items = StockItem.list(api, part=part.pk)

            if len(items) == 0:
                q = randint(0, 25)

                if q > 0:
                    StockItem.create(
                        api,
                        {
                            'part': part.pk,
                            'quantity': q,
                            'location': loc_id,
                        }
                    )

            # Generate parameters for each item
            Parameter.create(
                api,
                {
                    'part': part.pk,
                    'template': templates['Pitch'],
                    'data': p
                }
            )

            Parameter.create(
                api,
                {
                    'part': part.pk,
                    'template': templates['Positions'],
                    'data': n
                }
            )

            Parameter.create(
                api,
                {
                    'part': part.pk,
                    'template': templates['Rows'],
                    'data': r
                }
            )