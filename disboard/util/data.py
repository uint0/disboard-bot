import operator

def column_getters(column_meta, getter_columns, *, requires_all=True):
    getters = [None] * len(getter_columns)
    wanted = {col: i for i, col in enumerate(getter_columns)}

    for i, col in enumerate(column_meta):
        if col.name in wanted:
            getters[wanted[col.name]] = operator.itemgetter(i)

    if requires_all and any(w is None for w in wanted):
        raise ValueError("Not all getters were found")

    return getters
