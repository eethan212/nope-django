import pytz
from datetime import datetime
from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        display_fields = getattr(self, 'DisplayField', 'id')
        return "|".join(["%s: %s" % (field, getattr(self, field, "")) for field
                         in display_fields.split(",")])

    class Meta:
        abstract = True


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at=None)


class DeleteMixin(models.Model):
    deleted_at = models.DateTimeField("记录删除时间", null=True, blank=True, default=None)

    objects = DeletedManager()
    allobjects = models.Manager()

    @property
    def is_deleted(self):
        return True if self.deleted_at else False

    class Meta:
        abstract = True

    def _delete(self, using=None, keep_parents=False):
        super(DeleteMixin, self).delete()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now(pytz.UTC)
        self.save()
