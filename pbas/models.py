from django.db import models
from django.utils.crypto import get_random_string


class ProgressBar(models.Model):
    code = models.CharField(max_length=16, default=get_random_string, unique=True, db_index=True)
    title = models.CharField(max_length=32, blank=True)
    total = models.BigIntegerField()
    current = models.BigIntegerField(default=0)
    started = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def increment(self, amount=1):
        self.current = models.F('current') + amount

    @property
    def proportion(self):
        return self.current / self.total

    @property
    def run_time(self):
        return self.last_updated - self.started

    @property
    def estimate(self):
        return ((self.run_time / self.proportion) - self.run_time) if self.proportion else None

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.current = min((models.F('current'), self.total))
        super().save(force_insert, force_update, using, update_fields)

    def to_dict(self):
        estimate = self.estimate
        return {
            'title': self.title,
            'code': self.title,
            'total': self.total,
            'current': self.current,
            'proportion': self.current / self.total,
            'started': self.started,
            'last_updated': self.last_updated,
            'run_time': self.run_time.total_seconds(),
            'estimate': estimate.total_seconds() if estimate else None
        }

    class Meta:
        db_table = 'progress_bar'
