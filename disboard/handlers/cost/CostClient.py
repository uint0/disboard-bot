import datetime as dt

import azure.mgmt.costmanagement

import util.azure


class CostClient:
    def __init__(self):
        creds, subscription_id = util.azure.get_credentials()
        self._subscription_id = subscription_id
        self._cost_management = azure.mgmt.costmanagement.CostManagementClient(
            credential=creds,
            subscription_id=subscription_id
        )


    def report(
        self, *,
        scope=None,
        timeframe='custom',
        from_date: dt.datetime=None,
        to_date: dt.datetime=None,
        dataset: dict={}
    ):
        scope = scope or f'/subscriptions/{self._subscription_id}'

        return self._query_usage(
            scope,
            query_type='ActualCost',
            timeframe=timeframe,
            from_date=from_date,
            to_date=to_date,
            dataset=dataset
        )


    def credit(self):
        pass

    
    def _query_usage(
        self, scope, *,
        query_type: str='ActualCost',
        timeframe: str='custom',
        from_date: dt.datetime=None,
        to_date: dt.datetime=None,
        dataset: dict={}
    ):
        query = {
            'type': query_type,
            'dataset': dataset
        }

        if timeframe != 'last_invoice':
            query['timeframe'] = timeframe

        if timeframe == 'custom':
            query['timePeriod'] = {
                'from': from_date,
                'to':to_date
            }

        return self._cost_management.query.usage(scope, query)
