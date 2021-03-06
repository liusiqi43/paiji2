from django.db import models

from django.contrib.auth import get_user_model
from django.conf import settings

from django.utils.translation import ugettext as _
from django.utils.timezone import now

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from . import CACHE_KEY

try:
    User = get_user_model()
except:
    User = settings.AUTH_USER_MODEL


class Alert(models.Model):
    SUCCESS = 0
    INFO = 1
    WARNING = 2
    DANGER = 3
    TYPE_CHOICES = (
        (SUCCESS, _('Information+')),
        (INFO, _('Information')),
        (WARNING, _('Attention')),
        (DANGER, _('Attention+')),
    )
    title = models.CharField(
        _('Title'),
        max_length=60,
    )
    description = models.TextField(
        _('Description'),
    )
    type = models.SmallIntegerField(
        _('Type'),
        choices=TYPE_CHOICES,
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('author'),
    )
    posted_at = models.DateTimeField(
        _('Alert date'),
        default=now,
    )
    end_date = models.DateTimeField(
        _('End date'),
    )

    def get_type_name(self):
        return ['success', 'info', 'warning', 'danger'][self.type]

    def save(self, *args, **kwargs):
        super(Alert, self).save(*args, **kwargs)
        if self.end_date > now():
            key = make_template_fragment_key(CACHE_KEY)
            cache.delete(key)
