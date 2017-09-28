from django.db import models

class Judger(models.Model):
    max = models.IntegerField(default=4)
    ip = models.CharField(max_length=30, default='0.0.0.0')
    port = models.IntegerField(default=8888, blank=True, null=True)
    remote = models.BooleanField(default=False, blank=True)
    token = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = "judger"

    def __str__(self):
        return str(self.id) + '-' + self.ip + ':' + str(port)
