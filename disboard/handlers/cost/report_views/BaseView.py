import abc

import util.data
import util.time

class BaseView(abc.ABC):
    def __init__(self, start_date=None, end_date=None):
        self.use_dates(start_date, end_date)
    
    def use_dates(self, start_date, end_date):
        self._start_date = start_date
        self._end_date   = end_date
    
    def populate_dates_from_data(self, data):
        day_getter, = util.data.column_getters(
            data.columns,
            ['UsageDate']
        )

        all_dates = [util.time.from_int_date(day_getter(row)) for row in data.rows]

        self._start_date = min(all_dates)
        self._end_date   = max(all_dates)
    
    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @abc.abstractproperty
    def dataset(self):
        pass

    @abc.abstractmethod
    def render(self, data: dict):
        pass
