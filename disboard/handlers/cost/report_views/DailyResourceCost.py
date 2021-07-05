import io
import collections
import datetime as dt

import matplotlib.pyplot as plt

import util.data
import util.iter
import util.time
import util.azure

from . import BaseView

class DailyResourceCostView(BaseView.BaseView):
    dataset = {
        "aggregation": {
            "totalCost": {
                "function": "Sum",
                "name": "Cost"
            },
            "totalCostUSD": {
                "function": "Sum",
                "name": "CostUSD"
            }
        },
        "granularity": "Daily",
        "grouping": [
            {
                "name": "ResourceId",
                "type": "Dimension"
            },
            {
                "name": "ChargeType",
                "type": "Dimension"
            },
            {
                "name": "PublisherType",
                "type": "Dimension"
            }
        ],
        "sorting": [
            {
                "direction": "ascending",
                "name": "UsageDate"
            }
        ]
    }
    
    def render(self, data):
        if not (self._start_date or self._end_date):
            self.populate_dates_from_data(data)

        resource_daily_costs = self.get_resource_daily_costs(data)
        fig = self.make_figure(resource_daily_costs)

        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        return buf

    def get_resource_daily_costs(self, data):
        day_getter, cost_getter, resource_getter = util.data.column_getters(
            data.columns,
            ['UsageDate', 'Cost', 'ResourceId']
        )

        return {
            resource: collections.defaultdict(
                int,
                (
                    (
                        util.time.from_int_date(day_getter(day_info)),
                        cost_getter(day_info)
                    )
                    for day_info in sorted(costs, key=day_getter)
                )
            )
            for resource, costs in util.iter.group_all_by(
                data.rows,
                key=resource_getter
            )
        }


    def make_figure(self, resource_daily_costs):
        layers = []
        for name, cost in resource_daily_costs.items():
            layers.append((name, [
                cost[d]
                for d in util.iter.daterange(self._start_date, self._end_date, exclude=False)
            ]))
        
        date_labels = [
            d.strftime('%Y-%m-%d') for d in 
            util.iter.daterange(self._start_date, self._end_date, exclude=False)
        ]
        acc = [0] * len(layers[0][1])

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.set_ylabel('AUD')
        ax.set_title('Daily Resouce Costs')

        for name, layer in layers:
            ax.bar(
                date_labels,
                layer,
                bottom=acc,
                label=util.azure.resource_short_name(name)
            )
            acc = util.iter.elementsum(layer, acc)
        
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -1))

        ax.set_ylim(0, max(acc) + 1)
        for tick in ax.get_xticklabels():
            tick.set_rotation(330)

        return fig
