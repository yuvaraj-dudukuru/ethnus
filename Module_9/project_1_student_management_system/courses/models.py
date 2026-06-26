# ============================================================================
#  models.py — courses offered by the college.
# ============================================================================
from django.db import models


class Course(models.Model):
    """A course students can enrol in, e.g. 'Algorithms' (4 credits)."""

    title = models.CharField(max_length=120, unique=True)
    credits = models.PositiveIntegerField(default=3)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
