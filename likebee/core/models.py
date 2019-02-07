from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from mptt.models import MPTTModel, TreeForeignKey
from ..accounts.models import User


COLOR_TEXT_CHOICES = (
    ('#ffffff', _('Branco')),
    ('#000000', _('Preto')),
)


class TaskManager(models.Manager):
    def get_queryset(self):
        # return super().get_queryset().filter(
        #     Q(status=None) | Q(status__archive=False))
        return super().get_queryset().filter(arcived=False)


class ColorChoices(models.Model):
    name = models.CharField(
        _(u'Nome'), max_length=200
    )
    color = models.CharField(
        _(u'Cor'), max_length=7, default='#666666'
    )
    color_text = models.CharField(
        _(u'Cor do Texto'), choices=COLOR_TEXT_CHOICES,
        max_length=7, default='#ffffff'
    )
    order = models.PositiveIntegerField(
        _(u'Ordem'), default=0
    )

    class Meta:
        abstract = True
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Priority(ColorChoices):

    class Meta:
        verbose_name = _(u'Prioridade')
        verbose_name_plural = _(u'Prioridades')
        db_table = 'priority'


class Status(ColorChoices):
    done = models.BooleanField(
        _(u'Concluído?'), default=False
    )
    archive = models.BooleanField(
        _(u'Arquivado?'), default=False
    )

    class Meta:
        verbose_name = _(u'Status')
        verbose_name_plural = _(u'Status')
        db_table = 'status'


class Timestamp(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class meta:
        abstract = True


class Sprint(models.Model):
    name = models.CharField(
        _(u'Nome'), max_length=200, default='Sprint'
    )
    start_on = models.DateTimeField(
        _(u'Inicia em'), blank=True, null=True
    )
    finish_on = models.DateTimeField(
        _(u'Termina em'), blank=True, null=True
    )

    class Meta:
        ordering = ['-start_on', '-finish_on', 'name']
        verbose_name = _(u'Sprint')
        verbose_name_plural = _(u'Sprints')
        db_table = 'sprint'

    def __str__(self):
        return '{} - {}'.format(self.formatted_start, self.formatted_finish)

    @property
    def formatted_start(self):
        return self.start_on.strftime('%b %-d')

    @property
    def formatted_finish(self):
        return self.finish_on.strftime('%b %-d')


class Project(models.Model):
    name = models.CharField(
        _(u'Nome'), max_length=100
    )
    description = models.TextField(
        _(u'Descrição'), blank=True, null=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = _(u'Projeto')
        verbose_name_plural = _(u'Projetos')
        db_table = 'project'

    def __str__(self):
        return self.name


class TaskType(ColorChoices):

    class Meta:
        verbose_name = _(u'Tipo')
        verbose_name_plural = _(u'Tipos')
        db_table = 'task_type'


class Task(MPTTModel):
    sprint = models.ForeignKey(
        Sprint, verbose_name=_(u'Sprint'), related_name='tasks',
        on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(
        _(u'Título'), max_length=200
    )
    parent = TreeForeignKey(
        'self', verbose_name=_(u'Tarefa pai'), on_delete=models.CASCADE,
        blank=True, null=True, related_name='children'
    )
    description = models.TextField(
        _(u'Descrição'), blank=True, null=True
    )
    owner = models.ForeignKey(
        User, verbose_name=_(u'Responsável'), related_name='tasks',
        on_delete=models.CASCADE, blank=True, null=True
    )
    priority = models.ForeignKey(
        Priority, verbose_name=_(u'Prioridade'), related_name='tasks',
        on_delete=models.CASCADE, blank=True, null=True
    )
    task_type = models.ForeignKey(
        TaskType, verbose_name=_(u'Tipo'), related_name='tasks',
        on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.ForeignKey(
        Status, verbose_name=_(u'Status'), related_name='tasks',
        on_delete=models.CASCADE, blank=True, null=True
    )
    finish_on = models.DateTimeField(
        _(u'Prazo'), blank=True, null=True
    )
    project = models.ForeignKey(
        Project, verbose_name=_(u'Projeto'), related_name='tasks',
        on_delete=models.CASCADE, blank=True, null=True
    )
    time_estimate = models.DecimalField(
        _(u'Tempo'), max_digits=5, decimal_places=1,
        blank=True, null=True, help_text=_('Tempo estimado em horas')
    )
    archived = models.BooleanField(
        _(u'Arquivado?'), default=False
    )

    all_objects = models.Manager()
    objects = TaskManager()

    class Admin:
        manager = TaskManager()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        ordering = ['status', 'priority']
        verbose_name = _(u'Tarefa')
        verbose_name_plural = _(u'Tarefas')
        db_table = 'task'

    # def __str__(self):
    #     return '{} - {}'.format(self.sprint, self.title)
    def __str__(self):
        return self.title
