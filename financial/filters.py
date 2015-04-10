from django.db.models.query_utils import Q
from django.template.context import Context
from django.template.loader import get_template
import operator
from dashboard_view.listview_filters import DashboardListViewFilters


class FiEntryFilter(DashboardListViewFilters):
    pass