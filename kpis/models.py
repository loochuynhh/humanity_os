from django.db import models


class KPIs(models.Model):
    kpi_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "kpis"

    def __str__(self):
        return self.name
