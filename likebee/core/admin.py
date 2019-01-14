from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Priority, Status, Sprint, Project, Task


@admin.register(Task)
class TaskAdmin(SummernoteModelAdmin, DraggableMPTTAdmin):
    # change_list_template = 'admin/task_change_list.html'
    mptt_indent_field = 'title'

    list_per_page = 100
    list_display = [
        'tree_actions', 'indented_title',
        'owner_thumb', 'colored_priority', 'colored_status',
        'formatted_finish', 'project', 'time_estimate', 'sprint'
    ]
    list_display_links = [
        'indented_title',
    ]
    list_filter = [
        ('sprint', admin.RelatedFieldListFilter),
        ('owner', admin.RelatedFieldListFilter),
        ('project', admin.RelatedFieldListFilter),
    ]
    search_fields = ['title', 'description']
    summernote_fields = ['description']

    def formatted_finish(self, obj):
        if not obj.finish_on:
            return ''

        return obj.finish_on.strftime('%b %-d')

    formatted_finish.admin_order_field = 'finish_on'
    formatted_finish.short_description = _('Data')

    def colored_priority(self, obj):
        if obj.priority:
            name = obj.priority.name
            color = obj.priority.color
            color_text = obj.priority.color_text
        else:
            name = '-'
            color = '#C4C4C4'
            color_text = '#FFFFFF'
        return format_html(
            '<div style="background:{}; color:{}; ' \
            'text-align:center; padding: 4px;">{}</div>'.format(
                color, color_text, name))

    colored_priority.allow_tags = True
    colored_priority.admin_order_field = 'priority'
    colored_priority.short_description = _('Prioridade')

    def colored_status(self, obj):
        if obj.status:
            name = obj.status.name
            color = obj.status.color
            color_text = obj.status.color_text
        else:
            name = '-'
            color = '#C4C4C4'
            color_text = '#FFFFFF'
        return format_html(
            '<div style="background:{}; color:{}; ' \
            'text-align:center; padding: 4px;">{}</div>'.format(
                color, color_text, name))

    colored_status.allow_tags = True
    colored_status.admin_order_field = 'status'
    colored_status.short_description = _('Status')

    class Media:
        css = {
             'all': ('css/likebee.css',)
        }


admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Sprint)
admin.site.register(Project)

