from django.contrib import admin
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from datetime import date
from django_summernote.admin import SummernoteModelAdmin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Priority, Status, Sprint, Project, Task, TaskType
from ..accounts.models import Profile


def make_done(modeladmin, request, queryset):
    status = Status.objects.filter(done=True).first()
    queryset.update(status=status)


make_done.short_description = '''
    Marcar tarefas selecionadas como concluído'''


def make_archive(modeladmin, request, queryset):
    queryset.update(archived=True)


make_archive.short_description = '''
    Marcar tarefas selecionadas como arquivado'''


@admin.register(Task)
class TaskAdmin(SummernoteModelAdmin, DraggableMPTTAdmin):
    # change_list_template = 'admin/task_change_list.html'
    mptt_indent_field = 'title'

    list_per_page = 100
    list_display = [
        'tree_actions', 'indented_title',
        'owner_thumb', 'colored_priority', 'colored_status',
        'colored_task_type', 'formatted_finish', 'project', 'sprint'
    ]
    list_display_links = [
        'indented_title',
    ]
    list_filter = [
        ('sprint', admin.RelatedFieldListFilter),
        ('owner', admin.RelatedFieldListFilter),
        ('project', admin.RelatedFieldListFilter),
        ('status', admin.RelatedFieldListFilter),
        'archived',
    ]
    search_fields = ['title', 'description']
    summernote_fields = ['description']
    actions = [make_done, make_archive]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # return qs.filter(Q(status=None) | Q(status__archive=False))
        return qs.filter(archived=False)

    def formatted_finish(self, obj):
        if not obj.finish_on:
            return ''

        color = '#373A3C'

        status_done = None
        status = None
        if obj.status:
            status_done = obj.status.done
            status = obj.status

        if (obj.finish_on.date() < date.today()) and (
                not status_done or not status):
            color = '#E0465E'

        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>'.format(
                color, obj.finish_on.strftime('%b %-d')))

    formatted_finish.allow_tags = True
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
            '<div style="background:{}; color:{}; '
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
            '<div style="background:{}; color:{}; '
            'text-align:center; padding: 4px;">{}</div>'.format(
                color, color_text, name))

    colored_status.allow_tags = True
    colored_status.admin_order_field = 'status'
    colored_status.short_description = _('Status')

    def colored_task_type(self, obj):
        if obj.task_type:
            name = obj.task_type.name
            color = obj.task_type.color
            color_text = obj.task_type.color_text
        else:
            name = '-'
            color = '#C4C4C4'
            color_text = '#FFFFFF'
        return format_html(
            '<div style="background:{}; color:{}; '
            'text-align:center; padding: 4px;">{}</div>'.format(
                color, color_text, name))

    colored_task_type.allow_tags = True
    colored_task_type.admin_order_field = 'task_type'
    colored_task_type.short_description = _('Tipo')

    def owner_thumb(self, obj):
        if obj.owner:
            profile = Profile.objects.filter(user=obj.owner)
            for item in profile:
                if item.photo:
                    img = item.photo_thumbnail.url
                else:
                    img = None

                if img:
                    return format_html(
                        '<img src="{0}" width="35" />'.format(img)
                    )
            owner = obj.owner
        else:
            owner = ''

        return '{}'.format(owner)
    owner_thumb.allow_tags = True
    owner_thumb.admin_order_field = 'owner'
    owner_thumb.short_description = _('Resp.')

    class Media:
        css = {
             'all': ('css/likebee.css',)
        }


admin.site.register(Priority)
admin.site.register(Status)
admin.site.register(Sprint)
admin.site.register(Project)
admin.site.register(TaskType)
