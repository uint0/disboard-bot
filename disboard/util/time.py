import functools
import datetime as dt

@functools.singledispatch
def midnight(arg):
    raise ValueError

@midnight.register
def _(arg: dt.date):
    return dt.datetime.combine(arg, dt.datetime.min.time())

@midnight.register
def _(arg: dt.datetime):
    return arg.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

def from_int_date(int_date):
    return dt.datetime.strptime(str(int_date), '%Y%m%d')