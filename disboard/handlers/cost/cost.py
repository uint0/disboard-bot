import collections
import datetime as dt

import util.time

import handlers.cost.CostClient
import handlers.cost.report_views


ReportSpec = collections.namedtuple('ReportSpec', [
    'timeframe',
    'start_date',
    'end_date'
])


class Cost:
    def __init__(self):
        self._cost_client = handlers.cost.CostClient.CostClient()


    def report(
        self,
        view_name: str,
        report_spec: ReportSpec
    ):
        timeframe, start_date, end_date = report_spec
        if timeframe == 'custom':
            end_date   = end_date   or util.time.midnight(dt.date.today())
            start_date = start_date or (end_date - dt.timedelta(days=30))

        view = handlers.cost.report_views.get_view_by_name(view_name)(start_date, end_date)

        usage_info = self._cost_client.report(
            dataset=view.dataset,
            timeframe=timeframe,
            from_date=start_date,
            to_date=end_date
        )

        return view.render(usage_info)
    
    def list_views(self):
        return handlers.cost.report_views.list_views()

