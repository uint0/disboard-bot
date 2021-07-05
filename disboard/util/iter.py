import operator
import itertools
import datetime as dt


def group_all_by(iterable, *, key):
    return itertools.groupby(sorted(
        iterable,
        key=key
    ), key=key)


def daterange(start_date, end_date, exclude=True):
    for n in range(int((end_date - start_date).days) + (0 if exclude else 1)):
        yield start_date + dt.timedelta(n)


def elementsum(*lists):
    return list(map(operator.add, *lists))