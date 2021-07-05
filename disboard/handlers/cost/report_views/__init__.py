from . import DailyResourceCost

view_registry = {
    'daily_resource_cost': DailyResourceCost.DailyResourceCostView
}

def get_view_by_name(view_name):
    return view_registry[view_name]

def list_views():
    return list(view_registry.keys())