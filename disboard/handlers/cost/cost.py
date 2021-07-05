import collections
import datetime as dt
import dateutil as dtutil

import util.data
import util.time

import handlers.cost.CostClient
import handlers.cost.report_views

SUMMARY_VIEW = 'daily_resource_cost'
BILLING_PERIOD_LENGTH = dtutil.relativedelta.relativedelta(months=1)

ReportSpec = collections.namedtuple('ReportSpec', [
    'timeframe',
    'start_date',
    'end_date'
])

BillingPeriodSummary = collections.namedtuple('BillingPeriodSummary', [
    'start_date',
    'end_date',
    'latest_reported_date',
    'total_costs'
])


class Cost:
    def __init__(self):
        self._cost_client = handlers.cost.CostClient.CostClient()

    async def report(
        self,
        view_name: str,
        report_spec: ReportSpec
    ):
        timeframe, start_date, end_date = report_spec
        if timeframe == 'custom':
            end_date   = end_date   or util.time.midnight(dt.date.today())
            start_date = start_date or (end_date - dt.timedelta(days=30))

        view = handlers.cost.report_views.get_view_by_name(view_name)(start_date, end_date)

        usage_info = await self._cost_client.report(
            dataset=view.dataset,
            timeframe=timeframe,
            from_date=start_date,
            to_date=end_date
        )

        return view.render(usage_info)

    async def summary(self):
        view = handlers.cost.report_views.get_view_by_name(SUMMARY_VIEW)()
        usage_info = await self._cost_client.report(
            dataset=view.dataset,
            timeframe='last_invoice'
        )
        view.populate_dates_from_data(usage_info)
        cost_getter, = util.data.column_getters(usage_info.columns, ['Cost'])

        return BillingPeriodSummary(
            start_date=view.start_date,
            end_date=view.start_date + BILLING_PERIOD_LENGTH,
            latest_reported_date=view.end_date,
            total_costs=sum(cost_getter(r) for r in usage_info.rows)
        )

    def list_views(self):
        return handlers.cost.report_views.list_views()

