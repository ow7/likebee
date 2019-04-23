"""
Dashboard para o admin com controlcenter.

Nesse arquivo estao todos os widgets e funcoes para
os graficos e listas.
"""

from controlcenter import Dashboard, widgets
from likebee.core.models import Task


class EmptyDashboard(Dashboard):
    """Funcao em branco."""

    pass


class MyWidget0(widgets.Widget):
    """Widget test 0."""

    template_name = 'chart.html'


class MyWidget1(widgets.Widget):
    """Widget test 1."""

    template_name = 'chart.html'


# example
class ModelItemList(widgets.ItemList):
    """Widget para listar todas as tarefas."""

    model = Task
    # queryset = model.objects.all()
    list_display = ('pk', 'title')
    list_display_links = ('pk', 'title')
    # template_name = 'my_custom_template.html'


class MySingleBarChart(widgets.SingleBarChart):
    """Widget de tarefas concluidas."""

    values_list = ('pk', 'time_estimate')
    queryset = Task.objects.order_by('-done_on')
    limit_to = 3


class NonEmptyDashboard(Dashboard):
    """Dash non empty test."""

    widgets = [
        ModelItemList,
        MySingleBarChart,
        # MyWidget0,
        # widgets.Group([MyWidget1])
    ]
