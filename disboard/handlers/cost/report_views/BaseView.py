import abc


class BaseView(abc.ABC):
    def __init__(self, start_date=None, end_date=None):
        self.use_dates(start_date, end_date)
    
    def use_dates(self, start_date, end_date):
        self._start_date = start_date
        self._end_date   = end_date

    @abc.abstractproperty
    def dataset(self):
        pass

    @abc.abstractmethod
    def render(self, data: dict):
        pass
