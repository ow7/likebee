from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        'User', verbose_name=_(u'Usuário'), related_name='profile',
        on_delete=models.CASCADE, primary_key=True
    )
    photo = models.ImageField(
        _(u'Foto'), upload_to='profile'
    )
    photo_thumbnail = ImageSpecField(
        source='photo', processors=[ResizeToFill(100, 100)],
        format='JPEG', options={'quality': 75}
    )

    class Meta:
        ordering = ['user']
        verbose_name = _(u'Perfil')
        verbose_name_plural = _(u'Perfis')
        db_table = 'profile'

    def __str__(self):
        return self.user.username

    def admin_thumb(self):
        if self.photo:
            img = self.photo_thumbnail.url
        else:
            img = None

        if img:
            return format_html(
                '<img src="{0}" width="50" />'.format(img)
            )

        return format_html('<span>Sem foto</span>')
    admin_thumb.short_description = 'Foto'
